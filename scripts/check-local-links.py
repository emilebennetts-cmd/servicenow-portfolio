#!/usr/bin/env python3
"""Audit local HTML navigation and image references in the static portfolio.

Usage: python3 scripts/check-local-links.py
No network access or third-party dependencies required.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRS = {".git", "node_modules", ".venv", "venv"}
ATTRS = {"a": "href", "img": "src", "script": "src", "link": "href"}
class References(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"])
        if tag in ATTRS and data.get(ATTRS[tag]):
            self.refs.append((tag, data[ATTRS[tag]]))

def audit():
    failures = []
    pages = {}
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in IGNORE_DIRS for part in path.relative_to(ROOT).parts):
            continue
        parser = References()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            pages[path.resolve()] = parser
        except (UnicodeError, ValueError) as exc:
            failures.append(f"{path.relative_to(ROOT)}: parse error: {exc}")
    for path, parser in pages.items():
        for tag, raw in parser.refs:
            url = urlsplit(raw.strip())
            if url.scheme or url.netloc or raw.startswith("//"):
                continue
            if url.path.startswith(("data:", "mailto:", "tel:", "javascript:")):
                continue
            local = unquote(url.path)
            if not local and not url.fragment:
                continue
            target = (ROOT / local.lstrip("/")) if local.startswith("/") else (path.parent / local)
            if not local:
                target = path
            if target.is_dir():
                target = target / "index.html"
            target = target.resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{path.relative_to(ROOT)}: path escapes site: {raw}")
                continue
            if not target.is_file():
                failures.append(f"{path.relative_to(ROOT)}: missing {tag} target: {raw}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                failures.append(f"{path.relative_to(ROOT)}: missing anchor: {raw}")
    print(f"Audited {len(pages)} HTML pages; {len(failures)} issue(s).")
    for failure in failures:
        print("ERROR:", failure)
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(audit())
