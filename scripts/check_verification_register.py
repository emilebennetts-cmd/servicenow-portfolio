#!/usr/bin/env python3
"""Validate public verification claims without requiring third-party packages."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "evidence/public-verification-register.json"
VALID = {"source-only", "DEV-reported", "DEV-verified", "mock-only", "production-verified", "proposed"}

def validate(data, root=ROOT):
    errors = []
    if data.get("schema_version") != "1.0":
        errors.append("Unsupported register schema version")
    definitions = data.get("classification_definitions", {})
    if set(definitions) != VALID:
        errors.append("Classification definitions are incomplete")
    ids = set()
    for entry in data.get("items", []):
        key = entry.get("id")
        if not key or key in ids:
            errors.append(f"Missing or duplicate claim ID: {key}")
        ids.add(key)
        if entry.get("classification") not in VALID:
            errors.append(f"{key}: invalid classification")
        for field in ("title", "basis", "runtime_verification", "public_screenshot_status"):
            if not entry.get(field):
                errors.append(f"{key}: missing {field}")
        page = entry.get("page", "")
        if not page or Path(page).is_absolute() or ".." in Path(page).parts or not (root / page).is_file():
            errors.append(f"{key}: missing or unsafe case-study page {page}")
        if entry.get("classification") in {"DEV-verified", "production-verified"}:
            if not entry.get("verification_date") or not entry.get("verification_reference"):
                errors.append(f"{key}: independent verification requires dated evidence")
    if not ids:
        errors.append("Register contains no claims")
    return errors

if __name__ == "__main__":
    errors = validate(json.loads(REGISTER.read_text(encoding="utf-8")))
    for error in errors:
        print("FAIL:", error)
    print(f"Verification register: {len(errors)} issue(s)")
    raise SystemExit(bool(errors))
