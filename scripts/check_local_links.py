#!/usr/bin/env python3
"""Fail CI when a published HTML page references a missing local target.

Checks local href/src attributes and fragment IDs; does not request external URLs.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"mailto", "tel", "javascript", "data"}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append((key, a[key]))

def audit(root):
    pages = {}
    for path in root.rglob("*.html"):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        if not path.resolve().is_relative_to(root.resolve()):
            continue  # Never read symlinked HTML outside the publication root.
        p = Page()
        p.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = p
    errors = []
    for source, parsed in pages.items():
        for attribute, value in parsed.links:
            url = urlsplit(value)
            if url.scheme.lower() in SKIP or url.scheme or url.netloc or value.startswith("//"):
                continue
            if not url.path and not url.fragment:
                continue
            target = (root / unquote(url.path).lstrip("/")) if url.path.startswith("/") else (source.parent / unquote(url.path))
            if not url.path:
                target = source
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"{source.relative_to(root)}: {attribute} escapes site root: {value}")
            elif not target.is_file():
                errors.append(f"{source.relative_to(root)}: missing local target: {value}")
            elif url.fragment and target.suffix.lower() == ".html":
                if target not in pages:
                    p = Page()
                    p.feed(target.read_text(encoding="utf-8"))
                else:
                    p = pages[target]
                if unquote(url.fragment) not in p.ids:
                    errors.append(f"{source.relative_to(root)}: missing fragment: {value}")
    return errors

if __name__ == "__main__":
    problems = audit(ROOT)
    for problem in problems:
        print("ERROR:", problem)
    print(f"Local link audit: {'FAILED' if problems else 'PASSED'} ({len(problems)} issues)")
    sys.exit(bool(problems))
