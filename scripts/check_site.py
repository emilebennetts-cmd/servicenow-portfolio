#!/usr/bin/env python3
"""Dependency-free static portfolio link and accessibility smoke checks."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path(__file__).resolve().parents[1]
class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.ids=set(); self.duplicate_ids=set(); self.images=[]; self.title=False; self.lang=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="html": self.lang=bool(a.get("lang"))
        if tag=="title": self.title=True
        if a.get("id"):
            if a["id"] in self.ids: self.duplicate_ids.add(a["id"])
            self.ids.add(a["id"])
        if tag in ("a","link","script","img"):
            key={"a":"href","link":"href","script":"src","img":"src"}[tag]
            if a.get(key): self.links.append((tag,a[key]))
        if tag=="img": self.images.append(a)

def main():
    pages={p.relative_to(ROOT).as_posix():p for p in ROOT.rglob("*.html") if ".git" not in p.parts}
    parsed={}
    failures=[]
    for name,path in pages.items():
        doc=Inspector()
        try: doc.feed(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{name}: HTML parse error: {exc}");continue
        parsed[name]=doc
        for duplicate in sorted(doc.duplicate_ids): failures.append(f"{name}: duplicate id {duplicate}")
        if not doc.lang: failures.append(f"{name}: missing html lang")
        if not doc.title: failures.append(f"{name}: missing title")
        for img in doc.images:
            if not img.get("alt") and img.get("alt")!="":
                failures.append(f"{name}: image without alt attribute")
    for name,doc in parsed.items():
        for tag,href in doc.links:
            if href.startswith(("mailto:","tel:","data:","javascript:","//")): continue
            u=urlsplit(href)
            if u.scheme or u.netloc: continue  # external URLs checked separately
            target=unquote(u.path)
            if target.startswith("/"): continue  # site-root absolute URL; deployment dependent
            if not target and not u.fragment: continue
            path=(ROOT/name).parent/target if target else ROOT/name
            path=path.resolve()
            if not path.is_relative_to(ROOT.resolve()):
                failures.append(f"{name}: local reference escapes site root {href}")
                continue
            if path.is_dir(): path=path/"index.html"
            if not path.is_file():
                failures.append(f"{name}: broken local {tag} reference {href}")
                continue
            if u.fragment and path.suffix.lower()==".html":
                dest=path.relative_to(ROOT).as_posix()
                if dest in parsed and unquote(u.fragment) not in parsed[dest].ids:
                    failures.append(f"{name}: missing fragment {href}")
    print(f"Checked {len(parsed)} HTML pages; {len(failures)} issue(s).")
    for failure in failures: print("FAIL:",failure)
    return 1 if failures else 0

if __name__=="__main__": sys.exit(main())
