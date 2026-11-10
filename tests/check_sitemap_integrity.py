#!/usr/bin/env python3
"""Offline sitemap integrity gate for the GitHub Pages project site.

Checks that every declared public page exists, is unique, and stays within the
project URL prefix. Does not access the network or inspect private repositories.
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://emilebennetts-cmd.github.io/servicenow-portfolio/"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def validate(root=ROOT):
    errors = []
    try:
        tree = ET.parse(root / "sitemap.xml")
    except (ET.ParseError, OSError) as exc:
        return [f"Invalid sitemap: {exc}"]
    seen = set()
    entries = tree.findall(f".//{NS}loc")
    if not entries:
        return ["Sitemap contains no loc entries"]
    for node in entries:
        url = (node.text or "").strip()
        if url in seen:
            errors.append(f"Duplicate URL: {url}")
        seen.add(url)
        parts = urlsplit(url)
        if not url.startswith(BASE) or parts.query or parts.fragment:
            errors.append(f"Noncanonical project URL: {url}")
            continue
        relative = unquote(url[len(BASE):])
        if not relative or relative.endswith("/"):
            relative += "index.html"
        destination = (root / relative).resolve()
        if not destination.is_relative_to(root.resolve()):
            errors.append(f"Escaping sitemap path: {url}")
        elif not destination.is_file():
            errors.append(f"Missing sitemap target: {url}")
        elif destination.suffix != ".html":
            errors.append(f"Non-HTML sitemap target: {url}")
    return errors


if __name__ == "__main__":
    failures = validate()
    for failure in failures:
        print("ERROR:", failure)
    print(f"Sitemap integrity: {'FAIL' if failures else 'PASS'} ({len(failures)} finding(s))")
    sys.exit(bool(failures))
