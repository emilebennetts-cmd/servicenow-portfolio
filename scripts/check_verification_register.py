#!/usr/bin/env python3
"""Validate public verification claims without requiring third-party packages."""
import json
from datetime import date
from urllib.parse import urlparse
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
    root = Path(root).resolve()
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
        target = (root / page).resolve() if isinstance(page, str) and page else root
        if (not isinstance(page, str) or not page.endswith(".html") or Path(page).is_absolute()
                or ".." in Path(page).parts or not target.is_relative_to(root)
                or not target.is_file()):
            errors.append(f"{key}: missing or unsafe case-study page {page}")
        if entry.get("classification") in {"DEV-verified", "production-verified"}:
            when = entry.get("verification_date")
            reference = entry.get("verification_reference")
            if not when or not reference:
                errors.append(f"{key}: independent verification requires dated evidence")
            else:
                try:
                    verified_on = date.fromisoformat(when)
                    if verified_on > date.today():
                        errors.append(f"{key}: verification date cannot be in the future")
                except (TypeError, ValueError):
                    errors.append(f"{key}: verification date must be ISO YYYY-MM-DD")
                parsed = urlparse(reference) if isinstance(reference, str) else None
                if (not parsed or parsed.scheme != "https" or not parsed.netloc
                        or parsed.username or parsed.password):
                    errors.append(f"{key}: verification reference must be an HTTPS evidence URL")
            if entry.get("classification") == "production-verified" and not entry.get("production_authorisation"):
                errors.append(f"{key}: production verification requires authorisation record")
    if not ids:
        errors.append("Register contains no claims")
    return errors

if __name__ == "__main__":
    errors = validate(json.loads(REGISTER.read_text(encoding="utf-8")))
    for error in errors:
        print("FAIL:", error)
    print(f"Verification register: {len(errors)} issue(s)")
    raise SystemExit(bool(errors))
