#!/usr/bin/env python3
"""Fail-closed, offline freshness check for the curated public portfolio index.

--check keeps the hand-edited catalogue honest. --write adds missing pages
without replacing reviewed titles/keywords, and reconciles displayed counts.
No external requests, credentials, or private paths are needed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPLORER = "portfolio-explorer.html"
CATEGORIES = (
    "Start here", "Delivery", "Diagnostic", "Architecture",
    "Assurance", "Evidence & governance", "Labs & patterns",
)


class Rows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.current = None
        self.anchor = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "li" and "result" in a.get("class", "").split():
            if self.current is not None:
                raise ValueError("Nested portfolio result")
            self.current = {"category": a.get("data-category", ""),
                            "search": a.get("data-search", ""),
                            "links": [], "labels": []}
        elif self.current is not None and tag == "a":
            self.current["links"].append(a.get("href", ""))
            self.anchor = True

    def handle_data(self, data):
        if self.current is not None and self.anchor:
            self.current["labels"].append(data)

    def handle_endtag(self, tag):
        if self.current is not None and tag == "a":
            self.anchor = False
        elif self.current is not None and tag == "li":
            self.rows.append(self.current)
            self.current = None


def public_pages(root: Path) -> set[str]:
    return {p.name for p in root.glob("*.html") if p.is_file() and not p.is_symlink()
            and p.name != EXPLORER}


def catalogue_rows(source: str) -> list[dict]:
    parser = Rows()
    parser.feed(source)
    return parser.rows


def problems(root: Path, source: str) -> list[str]:
    rows = catalogue_rows(source)
    expected = public_pages(root)
    names = [r["links"][0] if len(r["links"]) == 1 else "" for r in rows]
    counts = Counter(names)
    errors = []
    for r in rows:
        if len(r["links"]) != 1:
            errors.append("Result must have exactly one link")
        if r["category"] not in CATEGORIES:
            errors.append("Unknown topic: " + r["category"])
        if not "".join(r["labels"]).strip():
            errors.append("Result has no link label")
        if r["links"] and r["links"][0].lower() not in r["search"].lower():
            errors.append("Search metadata omits filename: " + r["links"][0])
    for filename, count in counts.items():
        if count > 1:
            errors.append(f"Duplicate result: {filename} ({count})")
    for filename in sorted(expected - set(names)):
        errors.append("Missing page: " + filename)
    for filename in sorted(set(names) - expected):
        errors.append("Unknown/unpublished page: " + filename)
    total = len(expected)
    if not re.search(rf'Search {total} published pages\.', source):
        errors.append(f"Heading count stale (expected {total})")
    if not re.search(rf'<strong id="total">{total}</strong>', source):
        errors.append(f"Hero count stale (expected {total})")
    return errors


def category_for(filename: str) -> str:
    stem = filename.lower()
    if any(t in stem for t in ("screenshot", "evidence", "verification", "publication")):
        return "Evidence & governance"
    if any(t in stem for t in ("diagnostic", "cmdb", "rescan")):
        return "Diagnostic"
    if any(t in stem for t in ("architecture", "integration", "compatibility")):
        return "Architecture"
    if any(t in stem for t in ("pattern", "lab")):
        return "Labs & patterns"
    if any(t in stem for t in ("assurance", "acceptance", "readiness", "gate")):
        return "Assurance"
    if any(t in stem for t in ("delivery", "workbench", "incident", "itsm")):
        return "Delivery"
    return "Start here"


def title_for(path: Path) -> str:
    contents = path.read_text(encoding="utf-8")
    match = re.search(r"<title\b[^>]*>(.*?)</title>", contents, re.I | re.S)
    title = unescape(re.sub(r"<[^>]*>", "", match.group(1))).strip() if match else ""
    return title.split(" | ")[0].split(" — ")[0].strip() or path.stem.replace("-", " ").title()


def reconcile(root: Path, source: str) -> str:
    names = {r["links"][0] for r in catalogue_rows(source) if len(r["links"]) == 1}
    missing = sorted(public_pages(root) - names)
    if missing:
        open_tag = '<ul class="directory" id="results">'
        if source.count(open_tag) != 1:
            raise ValueError("Cannot locate one curated result list")
        end = source.find("</ul>", source.index(open_tag))
        if end < 0:
            raise ValueError("Catalogue list is not closed")
        added = []
        for filename in missing:
            category, title = category_for(filename), title_for(root / filename)
            query = f"{title} {category} {filename}".lower()
            added.append(
                f'<li class="result" data-category="{escape(category, quote=True)}" '
                f'data-search="{escape(query, quote=True)}">'
                f'<span class="type">{escape(category)}</span>'
                f'<a href="{escape(filename, quote=True)}">{escape(title)}</a>'
                f'<span class="locator">{escape(filename)}</span></li>'
            )
        source = source[:end] + "\n".join(added) + "\n" + source[end:]
    total = len(public_pages(root))
    source, head_count = re.subn(r"Search \d+ published pages\.", f"Search {total} published pages.", source, count=1)
    source, hero_count = re.subn(r'(<strong id="total">)\d+(</strong>)',
                                rf'\g<1>{total}\g<2>', source, count=1)
    if head_count != 1 or hero_count != 1:
        raise ValueError("Missing expected heading or hero count")
    return source


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = ap.parse_args()
    page = ROOT / EXPLORER
    source = page.read_text(encoding="utf-8")
    if args.write:
        source = reconcile(ROOT, source)
        if problems(ROOT, source):
            print("\n".join(problems(ROOT, source)), file=sys.stderr)
            return 1
        page.write_text(source, encoding="utf-8")
    errors = problems(ROOT, source)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Portfolio explorer reconciled: {len(public_pages(ROOT))} public pages, "
          f"{len(catalogue_rows(source))} unique results, no unindexed page")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
