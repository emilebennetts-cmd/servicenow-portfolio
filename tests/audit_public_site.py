#!/usr/bin/env python3
"""Offline site audit: local navigation, accessible structure and publication hygiene.

Run: python3 tests/audit_public_site.py [--strict]
Default reports findings; --strict exits nonzero for CI release gates.
No network access, credentials or third-party packages are required.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "node_modules", ".venv", "vendor"}
PRIVATE_MARKERS = ("servicenow-portfolio-control", "drive.google.com/file/d/",
                   "docs.google.com/document/d/")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.images, self.titles = set(), [], [], []
        self.duplicates = []
        self.viewport = False
        self.main = 0
        self._title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicates.append(a["id"])
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "img":
            self.images.append(a)
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag == "main":
            self.main += 1
        if tag == "title":
            self._title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False

    def handle_data(self, data):
        if self._title:
            self.titles.append(data)


def pages():
    return sorted(p for p in ROOT.rglob("*.html")
                  if not any(part in EXCLUDED or part.startswith(".")
                             for part in p.relative_to(ROOT).parts))


def audit():
    documents = {}
    for path in pages():
        parser = Page()
        source = path.read_text(encoding="utf-8")
        parser.feed(source)
        documents[path.resolve()] = (parser, source)
    findings = []
    for path, (page, source) in documents.items():
        name = str(path.relative_to(ROOT))
        def issue(code, detail):
            findings.append({"page": name, "code": code, "detail": detail})
        if not "".join(page.titles).strip():
            issue("missing-title", "Page has no nonempty title")
        if not page.viewport:
            issue("missing-viewport", "Mobile viewport declaration missing")
        if page.main != 1:
            issue("main-landmark", f"Expected one main landmark, found {page.main}")
        for identifier in page.duplicates:
            issue("duplicate-id", identifier)
        for marker in PRIVATE_MARKERS:
            if marker in source.lower():
                issue("private-reference", marker)
        for img in page.images:
            if "alt" not in img:
                issue("missing-image-alt", img.get("src", "(no src)"))
        resources = [(href, "link") for href in page.hrefs] + [(img.get("src", ""), "image") for img in page.images if img.get("src")]
        for href, kind in resources:
            target = urlsplit(href)
            if target.scheme.lower() in ("javascript", "data", "vbscript"):
                issue("unsafe-resource-url", f"{kind}: {href[:160]}")
                continue
            if target.scheme or target.netloc or href.startswith("//"):
                continue
            if not target.path and not target.fragment:
                continue
            relative = unquote(target.path)
            if relative.startswith("/"):
                # GitHub Pages project sites use a subpath; avoid silently approving ambiguous absolute links.
                issue("root-absolute-resource", f"{kind}: {href}")
                continue
            destination = (path.parent / relative).resolve() if relative else path
            if relative and destination.is_dir():
                destination = destination / "index.html"
            if not destination.is_relative_to(ROOT.resolve()):
                issue("path-escape", href)
                continue
            if not destination.is_file():
                issue("missing-local-target", f"{kind}: {href}")
                continue
            if target.fragment and destination.suffix.lower() == ".html":
                target_page = documents.get(destination)
                if target_page and unquote(target.fragment) not in target_page[0].ids:
                    issue("missing-fragment", href)
    return {"pages_checked": len(documents), "finding_count": len(findings),
            "findings": findings}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--strict", action="store_true", help="Fail if any findings exist")
    args = cli.parse_args()
    result = audit()
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if args.strict and result["finding_count"] else 0)
