#!/usr/bin/env python3
"""Validate public verification claims without requiring third-party packages."""
import json
import re
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
            # These checks validate the *metadata contract*, never the truth of
            # a reviewer statement. A passing manifest is not native acceptance.
            commit = entry.get("source_commit_sha")
            if not isinstance(commit, str) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit):
                errors.append(f"{key}: verified claim requires a full lowercase source commit SHA")
            version = entry.get("installed_version")
            if not isinstance(version, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,39}", version):
                errors.append(f"{key}: verified claim requires installed application version")
            scope = entry.get("application_scope")
            if not isinstance(scope, str) or not re.fullmatch(r"(?:global|x_[a-z0-9_]{3,60})", scope):
                errors.append(f"{key}: verified claim requires valid ServiceNow application scope")
            environment = entry.get("execution_environment")
            expected = "PROD" if entry.get("classification") == "production-verified" else "DEV"
            if environment != expected:
                errors.append(f"{key}: verified claim requires execution_environment {expected}")
            alias = entry.get("environment_alias")
            if not isinstance(alias, str) or not re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{2,39}", alias):
                errors.append(f"{key}: verified claim requires safe anonymised environment alias")
            cases = entry.get("executed_test_ids")
            if not isinstance(cases, list) or not 1 <= len(cases) <= 40 or any(
                not isinstance(case, str) or not re.fullmatch(r"[A-Z][A-Z0-9_-]{1,39}", case)
                for case in cases
            ) or len(set(cases)) != len(cases):
                errors.append(f"{key}: verified claim requires unique executed test IDs")
            receipt = entry.get("evidence_receipt_alias")
            if not isinstance(receipt, str) or not re.fullmatch(r"[A-Z0-9][A-Z0-9_.-]{2,79}", receipt) or ".." in receipt:
                errors.append(f"{key}: verified claim requires safe private evidence receipt alias")
            if entry.get("independent_review_approved") is not True:
                errors.append(f"{key}: verified claim requires independent review approval metadata")

    if not ids:
        errors.append("Register contains no claims")
    return errors

if __name__ == "__main__":
    errors = validate(json.loads(REGISTER.read_text(encoding="utf-8")))
    for error in errors:
        print("FAIL:", error)
    print(f"Verification register: {len(errors)} issue(s)")
    raise SystemExit(bool(errors))
