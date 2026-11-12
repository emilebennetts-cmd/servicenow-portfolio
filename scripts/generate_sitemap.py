#!/usr/bin/env python3
"""Deterministic GitHub Pages sitemap generator for published root HTML pages.

Usage:
    python scripts/generate_sitemap.py --check   # CI, read-only
    python scripts/generate_sitemap.py --write   # local authoring
No network or private repository access is required.
"""
import argparse
from pathlib import Path
from urllib.parse import quote
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://emilebennetts-cmd.github.io/servicenow-portfolio/"
SITEMAP = ROOT / "sitemap.xml"


def public_pages(root=ROOT):
    """Root-level published HTML only; do not follow symlinks or crawl docs."""
    root = Path(root).resolve()
    pages = sorted(
        p.name for p in root.glob("*.html")
        if p.is_file() and not p.is_symlink() and p.parent == root
    )
    if "index.html" not in pages:
        raise ValueError("Published site is missing index.html")
    return ["index.html"] + [name for name in pages if name != "index.html"]


def render(root=ROOT):
    pages = public_pages(root)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name in pages:
        path = "" if name == "index.html" else quote(name, safe="-._~")
        lines.append(f"  <url><loc>{BASE}{path}</loc></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Check committed sitemap matches root HTML inventory")
    mode.add_argument("--write", action="store_true", help="Regenerate sitemap from root HTML inventory")
    args = parser.parse_args(argv)
    desired = render()
    if args.write:
        SITEMAP.write_text(desired, encoding="utf-8")
        print(f"Updated {SITEMAP.name}: {len(public_pages())} canonical pages")
        return 0
    current = SITEMAP.read_text(encoding="utf-8") if SITEMAP.is_file() else ""
    if current != desired:
        print("FAIL: sitemap.xml is stale, incomplete or nondeterministic.")
        print(f"Expected {len(public_pages())} canonical pages; regenerate using: python scripts/generate_sitemap.py --write")
        return 1
    print(f"PASS: sitemap.xml matches all {len(public_pages())} published root HTML pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
