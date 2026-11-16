#!/usr/bin/env python3
"""Anonymous post-deploy HTTPS verification. No ServiceNow access or credentials."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import ssl
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

BASE = "https://emilebennetts-cmd.github.io/servicenow-portfolio/"
MARKER = 'name="portfolio-publish-probe" content="https-gate-v1-20261115"'
TARGETS = {
    "index.html": MARKER,
    "delivery-release-evolution.html": 'id="package-fingerprint"',
    "diagnostic-workbench-case-study.html": 'id="diagnostic-operator"',
    "visual-evidence.html": 'id="gallery"',
    "delivery-case-study.html": 'id="delivery-plan-lab"',
    "reusable-delivery-patterns-case-study.html": 'id="pattern-fit-desk"',
    "diagnostic-delivery-handoff-contract.html": 'id="handoff-controls"',
    "cmdb-ire-assurance.html": 'id="acceptance"',
    "cmdb-tag-governance-lab.html": 'id="tag-lab"',
    "itsm-greenfield-build-sequencer.html": 'id="readiness"',
    "ki-matrix-intake.html": 'id="matrix-file"',
    "technical-evidence-register.html": 'id="source-lineage"',
    "portfolio-review-guide.html": 'id="review-route"',
    "problem-management-implementation-lab.html": 'id="lab"',
    "incident-management-implementation-lab.html": 'id="lab"',
}
RECEIPT = "public-https-smoke-receipt.json"
MAX_BYTES = 1_500_000


def validate_response(url, final_url, status, content_type, raw, required, expected_sha256=None):
    """Confirm canonical delivery; optionally require byte equality with checked-out HTML."""
    requested, final = urlparse(url), urlparse(final_url)
    # Strictly pin anonymous public responses to a canonical URL. A matching
    # hostname alone cannot exclude a different port, credentials or query.
    if (requested.scheme != "https" or requested.hostname != urlparse(BASE).hostname
            or requested.port is not None or requested.username is not None
            or requested.password is not None or requested.query or requested.fragment):
        raise ValueError("noncanonical requested URL")
    if (final.port is not None or final.username is not None or final.password is not None
            or final.query or final.fragment):
        raise ValueError("unexpected redirect URL metadata")
    if status != 200:
        raise ValueError(f"HTTP status {status}")
    if final.scheme != "https" or final.hostname != requested.hostname or final.path != requested.path:
        raise ValueError("HTTPS host or path changed unexpectedly")
    if content_type.split(";", 1)[0].strip().lower() != "text/html":
        raise ValueError("response is not HTML")
    if len(raw) > MAX_BYTES:
        raise ValueError("response exceeds safe inspection size")
    html = raw.decode("utf-8", errors="strict")
    if required not in html:
        raise ValueError("required published marker missing (deployment may be stale)")
    if expected_sha256 is not None and hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("published HTML bytes differ from checked-out source")


def live_check(name, required):
    # Compare GitHub Pages bytes to the exact file checked out at GITHUB_SHA,
    # not just a stable HTML marker that an outdated page could also contain.
    source = (Path(__file__).resolve().parents[1] / name).read_bytes()
    if len(source) > MAX_BYTES or required.encode("utf-8") not in source:
        raise ValueError("checked-out source is missing marker or exceeds size limit")
    source_digest = hashlib.sha256(source).hexdigest()
    url = BASE if name == "index.html" else BASE + name
    request = Request(url, headers={"User-Agent": "ServiceNow-Portfolio-Public-URL-Smoke/1.1",
                                    "Accept": "text/html", "Cache-Control": "no-cache"})
    with urlopen(request, timeout=15, context=ssl.create_default_context()) as response:
        raw = response.read(MAX_BYTES + 1)
        validate_response(url, response.geturl(), response.status,
                          response.headers.get("Content-Type", ""), raw, required,
                          expected_sha256=source_digest)
    return {"route": name, "url": url, "status": "PASS", "http_status": 200,
            "bytes_match_checkout": True, "sha256": source_digest}


def local_check(root):
    findings = []
    for name, required in TARGETS.items():
        content = (root / name).read_text(encoding="utf-8")
        if required not in content:
            raise ValueError(f"{name}: required marker missing")
        findings.append({"route": name, "status": "PASS", "verification": "LOCAL-ONLY"})
    return findings


def run_live(attempts, delay):
    pending = dict(TARGETS)
    successes, errors = {}, {}
    for attempt in range(1, attempts + 1):
        for name, required in list(pending.items()):
            try:
                successes[name] = live_check(name, required)
                del pending[name]
                errors.pop(name, None)
                print(f"PASS {name}: anonymous HTTPS 200 and published HTML marker")
            except (HTTPError, URLError, ValueError, UnicodeError, TimeoutError, OSError) as exc:
                # Never log page bodies, headers, cookies, credentials or URL parameters.
                errors[name] = type(exc).__name__
                print(f"RETRY {attempt}/{attempts} {name}: {type(exc).__name__}")
        if not pending:
            break
        if attempt < attempts:
            time.sleep(delay)
    results = [successes.get(n, {"route": n, "url": BASE if n == "index.html" else BASE + n,
                                 "status": "UNCONFIRMED",
                                 "failure_type": errors.get(n, "Unknown")}) for n in TARGETS]
    return results, not pending


def write_summary(results, success, mode):
    # Receipt integrity is a separate contract from the loop's success flag.
    # Never promote an incomplete/forged set of rows into a website-verified claim.
    route_names = [row.get("route") for row in results]
    full_live_set = bool(
        mode == "live" and success
        and len(results) == len(TARGETS)
        and len(set(route_names)) == len(TARGETS)
        and set(route_names) == set(TARGETS)
        and all(
            row.get("status") == "PASS"
            and row.get("http_status") == 200
            and row.get("url") == (BASE if row.get("route") == "index.html"
                                  else BASE + row.get("route", ""))
            for row in results
        )
    )
    exact_deployed_set = bool(
        full_live_set and all(
            row.get("bytes_match_checkout") is True
            and isinstance(row.get("sha256"), str)
            and len(row["sha256"]) == 64
            and all(ch in "0123456789abcdef" for ch in row["sha256"])
            for row in results
        )
    )
    output = {
        "schema_version": "1.0",
        "probe": "anonymous_public_https",
        "source_commit": os.environ.get("GITHUB_SHA", "unknown"),
        "execution": mode,
        "verified_live_public_website": full_live_set,
        "verified_exact_deployed_bytes": exact_deployed_set,
        "native_dev_verified": False,
        "production_servicenow_verified": False,
        "screenshot_publication_approved": False,
        "results": results,
    }
    Path(RECEIPT).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as handle:
            handle.write("## Public portfolio HTTPS smoke\n\n")
            handle.write(f"- Check type: **{mode}** (not native ServiceNow acceptance)\n")
            for row in results:
                handle.write(f"- {row['route']}: **{row['status']}**\n")
            handle.write(f"- Anonymous public URL: **{'CONFIRMED' if output['verified_live_public_website'] else 'UNCONFIRMED'}**\n")
            handle.write(f"- Exact deployed HTML bytes match checkout: **{'CONFIRMED' if output['verified_exact_deployed_bytes'] else 'UNCONFIRMED'}**\n")
            handle.write("- Native DEV, production and screenshot approval: **NOT VERIFIED / HOLD**\n")
    print(json.dumps({"live_public_website_confirmed": output["verified_live_public_website"],
                      "exact_deployed_bytes_confirmed": output["verified_exact_deployed_bytes"],
                      "routes_passed": sum(x["status"] == "PASS" for x in results),
                      "routes_total": len(results)}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("local", "live"), required=True)
    parser.add_argument("--attempts", type=int, default=8)
    parser.add_argument("--retry-seconds", type=int, default=15)
    args = parser.parse_args()
    if args.attempts < 1 or args.attempts > 20 or args.retry_seconds < 0 or args.retry_seconds > 60:
        parser.error("retry settings out of range")
    try:
        if args.mode == "local":
            results = local_check(Path(__file__).resolve().parents[1])
            success = True
        else:
            results, success = run_live(args.attempts, args.retry_seconds)
    except (OSError, ValueError, UnicodeError) as exc:
        results = [{"route": "local-files", "status": "FAIL",
                    "failure_type": type(exc).__name__}]
        success = False
    write_summary(results, success, args.mode)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
