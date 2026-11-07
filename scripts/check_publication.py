#!/usr/bin/env python3
"""Regression checks for the portfolio's public-content publication boundary.

This deliberately checks only tracked web assets, not private repositories.
It is a heuristic guardrail, not a substitute for human screenshot review.
"""
from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WEB_EXTENSIONS = {".html", ".htm", ".js", ".css", ".json", ".svg"}
SKIP_DIRS = {".git", ".github", "__pycache__", "node_modules"}
SENSITIVE = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b")),
    ("ServiceNow instance password assignment", re.compile(r"(?i)\b(?:password|passwd|client_secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]")),
]
# Public image assets must be manually reviewed and recorded before publication.
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
# Existing images are not automatically deemed safe; the gate flags new ones via a
# separately maintained reviewed-image allowlist. No unreviewed image is permitted.
ALLOWLIST = ROOT / "evidence" / "approved-public-images.txt"
# Each approval must bind the reviewed image bytes to its public path.
# Format: relative/path.png <sha256 hex digest>

def scan_text(text):
    return [label for label, pattern in SENSITIVE if pattern.search(text)]

def check(root=ROOT, allowlist=ALLOWLIST):
    issues = []
    approved = {}
    if allowlist.is_file():
        for line_number, raw in enumerate(allowlist.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split()
            if len(fields) != 2 or not re.fullmatch(r"[a-fA-F0-9]{64}", fields[1]):
                issues.append(f"approval manifest line {line_number}: expected path and SHA-256 digest")
                continue
            relative_path, digest = fields
            if relative_path in approved:
                issues.append(f"approval manifest line {line_number}: duplicate path {relative_path}")
            approved[relative_path] = digest.lower()
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            if relative not in approved:
                issues.append(f"{relative}: image lacks recorded publication approval")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != approved[relative]:
                issues.append(f"{relative}: image bytes changed since publication approval")
        if path.suffix.lower() in WEB_EXTENSIONS:
            try:
                contents = path.read_text(encoding="utf-8")
            except UnicodeError:
                issues.append(f"{relative}: invalid UTF-8 public asset")
                continue
            for label in scan_text(contents):
                issues.append(f"{relative}: potential {label} in public asset")
    for relative in approved:
        target = root / relative
        if (not target.is_file() or target.suffix.lower() not in IMAGE_EXTENSIONS
                or ".." in Path(relative).parts or Path(relative).is_absolute()):
            issues.append(f"{relative}: approval entry does not reference a valid public image")
    return issues

def main():
    issues = check()
    for issue in issues:
        print("FAIL:", issue)
    print(f"Public asset publication gate: {len(issues)} issue(s).")
    return int(bool(issues))

if __name__ == "__main__":
    sys.exit(main())
