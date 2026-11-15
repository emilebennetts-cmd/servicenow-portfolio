#!/usr/bin/env python3
"""Anonymous post-deploy HTTPS verification. No ServiceNow access or credentials."""
import argparse
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
}
RECEIPT = "public-https-smoke-receipt.json"
MAX_BYTES = 1_500_000


def validate_response(url, final_url, status, content_type, raw, required):
    """Confirm an anonymous 200, same HTTPS origin/path and current HTML."""
    requested, final = urlparse(url), urlparse(final_url)
    if status != 200:
        raise ValueError(f"HTTP status {status}")
    if final.scheme != "https" or final.hostname != requested.hostname or final.path != requested.path:
        raise ValueError("HTTPS host or path changed unexpectedly")
    if "text/html" not in content_type.lower():
        raise ValueError("response is not HTML")
    if len(raw) > MAX_BYTES:
        raise ValueError("response exceeds safe inspection size")
    html = raw.decode("utf-8", errors="strict")
    if required not in html:
        raise ValueError("required published marker missing (deployment may be stale)")


def live_check(name, required):
    url = BASE if name == "index.html" else BASE + name
    request = Request(url, headers={"User-Agent": "ServiceNow-Portfolio-Public-URL-Smoke/1.0",
                                    "Accept": "text/html", "Cache-Control": "no-cache"})
    with urlopen(request, timeout=15, context=ssl.create_default_context()) as response:
        raw = response.read(MAX_BYTES + 1)
        validate_response(url, response.geturl(), response.status,
                          response.headers.get("Content-Type", ""), raw, required)
    return {"route": name, "url": url, "status": "PASS", "http_status": 200}


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
    output = {
        "schema_version": "1.0",
        "probe": "anonymous_public_https",
        "source_commit": os.environ.get("GITHUB_SHA", "unknown"),
        "execution": mode,
        "verified_live_public_website": bool(success and mode == "live"),
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
            handle.write(f"- Anonymous public URL: **{'CONFIRMED' if success and mode == 'live' else 'UNCONFIRMED'}**\n")
            handle.write("- Native DEV, production and screenshot approval: **NOT VERIFIED / HOLD**\n")
    print(json.dumps({"live_public_website_confirmed": output["verified_live_public_website"],
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
