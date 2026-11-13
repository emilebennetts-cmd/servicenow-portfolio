#!/usr/bin/env python3
"""Offline, deterministic public claim annotation for the Portfolio Explorer.

The PUBLIC verification register is the sole source for labels. This tool
never loads private repositories, Drive files, credentials or ServiceNow data.
A page with multiple different registered claims is MIXED, never automatically
promoted to the highest status. No registered claim means NOT REGISTERED.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPLORER = ROOT / "portfolio-explorer.html"
REGISTER = ROOT / "evidence" / "public-verification-register.json"
LABELS = {
    "source-only": ("source-only", "SOURCE-ONLY"),
    "mock-only": ("mock-only", "MOCK-ONLY"),
    "DEV-reported": ("dev-reported", "DEV-REPORTED"),
    "DEV-verified": ("dev-verified", "DEV-VERIFIED"),
    "production-verified": ("production-verified", "PRODUCTION-VERIFIED"),
    "proposed": ("proposed", "PROPOSED"),
}
MIXED = ("mixed", "MIXED CLAIMS")
UNREGISTERED = ("unregistered", "NOT REGISTERED")
ROW = re.compile(r'(<li class="result"(?:\s[^>]*)?>)(.*?)(</li>)', re.S)
ANCHOR = re.compile(r'<a href="([^"]+\.html)"')
LOCATOR = re.compile(r'(<span class="locator">[^<]*</span>)')
PROOF = re.compile(r'<span class="proof"[^>]*>[^<]*</span>')


def claim_map(register: dict) -> dict[str, tuple[str, str]]:
    if not isinstance(register.get("items"), list):
        raise ValueError("Public verification register has no items array")
    by_page = defaultdict(set)
    for item in register["items"]:
        page, kind = item.get("page"), item.get("classification")
        if kind not in LABELS or not isinstance(page, str) or not re.fullmatch(r"[a-z0-9-]+\.html", page):
            raise ValueError("Invalid public claim page/classification")
        by_page[page].add(kind)
    return {page: LABELS[next(iter(kinds))] if len(kinds) == 1 else MIXED
            for page, kinds in by_page.items()}


def annotate(source: str, register: dict) -> str:
    labels = claim_map(register)
    count = 0
    def render(match: re.Match) -> str:
        nonlocal count
        opening, content, closing = match.groups()
        link = ANCHOR.search(content)
        if not link or not LOCATOR.search(content):
            raise ValueError("Explorer card is missing a valid public HTML link or locator")
        status, label = labels.get(link.group(1), UNREGISTERED)
        opening = re.sub(r'\sdata-evidence="[^"]*"', "", opening)
        opening = opening[:-1] + f' data-evidence="{status}">'
        content = PROOF.sub("", content)
        content = LOCATOR.sub(lambda m: m.group(1) + f'<span class="proof">{escape(label)}</span>', content, count=1)
        count += 1
        return opening + content + closing
    output = ROW.sub(render, source)
    if count == 0:
        raise ValueError("No result cards could be found")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    contents = EXPLORER.read_text(encoding="utf-8")
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    rendered = annotate(contents, register)
    if args.write:
        EXPLORER.write_text(rendered, encoding="utf-8")
    elif contents != rendered:
        print("FAIL: Explorer evidence labels diverge from public register. Run --write.")
        return 1
    print(f"PASS: public evidence annotations reconciled for {len(ROW.findall(rendered))} cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
