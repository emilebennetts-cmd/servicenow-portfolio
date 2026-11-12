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
WEB_EXTENSIONS = {".html", ".htm", ".js", ".css", ".json", ".svg", ".md", ".markdown"}
SKIP_DIRS = {".git", ".github", "__pycache__", "node_modules"}
SENSITIVE = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b")),
    ("ServiceNow instance password assignment", re.compile(r"(?i)\b(?:password|passwd|client_secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]")),
]

# Fail closed on hidden image pixels in HTML/CSS/JS/JSON/SVG, even when no
# standalone image file exists. Illustrative vector markup is allowed; it is
# still subject to confidentiality review. This is a heuristic CI guard,
# not pixel analysis or an authorisation mechanism.
VISUAL_EMBED_PATTERNS = [
    ("embedded image data URL", re.compile(r"(?i)\bdata\s*:\s*image\s*/")),
    ("remote image element", re.compile(
        r"(?is)<(?:img|source|image)\b[^>]*\b(?:src|srcset|href|xlink:href)\s*=\s*['\"]?\s*(?:https?:)?//"
    )),
    ("embedded foreignObject element", re.compile(r"(?i)<\s*foreignObject\b")),
    ("SVG image element", re.compile(r"(?i)<\s*image\b")),
    ("remote SVG use reference", re.compile(
        r"(?is)<\s*use\b[^>]*\b(?:href|xlink:href)\s*=\s*['\"]?\s*(?:https?:)?//"
    )),
    ("remote CSS background image", re.compile(
        r"(?is)\b(?:background(?:-image)?|mask(?:-image)?)\s*:\s*[^;{}]{0,500}?\burl\s*\(\s*['\"]?\s*(?:https?:)?//"
    )),
    # Inline SVG filters can display images without an <image> element.
    ("SVG filter image element", re.compile(r"(?i)<\s*feImage\b")),
    # An external video poster is an image even if no <img> exists.
    ("remote video poster", re.compile(
        r"(?is)<\s*video\b[^>]*\bposter\s*=\s*['\"]?\s*(?:https?:)?//"
    )),
    # CSS image-bearing properties other than background/mask can inject pixels.
    ("remote CSS image property", re.compile(
        r"(?is)\b(?:content|list-style-image|border-image-source|cursor)\s*:\s*[^;{}]{0,500}?\burl\s*\(\s*['\"]?\s*(?:https?:)?//"
    )),
]
# Browsing-context embeds can render arbitrary unreviewed pages or screenshots.
# They are not required by this static, offline-first public portfolio.
ACTIVE_HTML_EMBED_PATTERNS = [
    ("active HTML embed", re.compile(r"(?is)<\s*(?:iframe|object|embed)\b")),
]
SVG_UNSAFE_PATTERNS = [
    ("SVG image element", re.compile(r"(?i)<\s*image\b")),
    ("SVG executable script", re.compile(r"(?i)<\s*script\b")),
    ("SVG remote reference", re.compile(
        r"(?is)\b(?:href|xlink:href)\s*=\s*['\"]?\s*(?:https?:)?//"
    )),
    ("SVG CSS remote image", re.compile(r"(?is)\burl\s*\(\s*['\"]?\s*(?:https?:)?//")),
]

# Public image assets must be manually reviewed and recorded before publication.
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
MAX_PUBLIC_IMAGE_BYTES = 8 * 1024 * 1024  # guard against accidental raw exports

def image_format_matches(path, data):
    """Reject files disguised with an image suffix; no external dependencies."""
    suffix = path.suffix.lower()
    if suffix == ".png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return data.startswith(b"\xff\xd8\xff") and data.endswith(b"\xff\xd9")
    if suffix == ".webp":
        return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    if suffix == ".gif":
        return data.startswith((b"GIF87a", b"GIF89a"))
    if suffix == ".bmp":
        return data.startswith(b"BM")
    if suffix in {".tif", ".tiff"}:
        return data.startswith((b"II*\x00", b"MM\x00*"))
    return False
def embedded_metadata_markers(path, data):
    """Conservative markers for common image metadata containers.

    This is not a complete parser. A clean result cannot establish that a
    screenshot has been sanitised; human review remains mandatory.
    """
    suffix = path.suffix.lower()
    markers = []
    if suffix == ".png":
        for chunk in (b"tEXt", b"zTXt", b"iTXt", b"eXIf"):
            if chunk in data:
                markers.append(chunk.decode("ascii"))
    elif suffix in {".jpg", ".jpeg"}:
        for label, token in (("EXIF", b"Exif\x00\x00"), ("XMP", b"http://ns.adobe.com/xap/1.0/"),
                             ("Photoshop", b"Photoshop 3.0")):
            if token in data:
                markers.append(label)
    elif suffix == ".webp":
        for chunk in (b"EXIF", b"XMP "):
            if chunk in data:
                markers.append(chunk.decode("ascii").strip())
    elif suffix == ".gif" and b"\x21\xfe" in data:
        markers.append("GIF comment")
    return markers

# Existing images are not automatically deemed safe; the gate flags new ones via a
# separately maintained reviewed-image allowlist. No unreviewed image is permitted.
ALLOWLIST = ROOT / "evidence" / "approved-public-images.txt"
# Each approval must bind the reviewed image bytes to its public path.
# Format: relative/path.png <sha256 hex digest>

def scan_text(text):
    return [label for label, pattern in SENSITIVE if pattern.search(text)]

def scan_visual_embeds(text, suffix):
    """Catch common unreviewed screenshot-pixel bypasses; return finding labels."""
    checks = (VISUAL_EMBED_PATTERNS
              + (ACTIVE_HTML_EMBED_PATTERNS if suffix in {".html", ".htm"} else [])
              + (SVG_UNSAFE_PATTERNS if suffix == ".svg" else []))
    return [label for label, pattern in checks if pattern.search(text)]

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
            candidate = Path(relative_path)
            # Only canonical, repository-relative image paths are eligible.
            # Reject traversal, alternate separators, and paths outside the
            # dedicated screenshot directory before inspecting any bytes.
            if (candidate.is_absolute() or "\\" in relative_path
                    or any(part in {".", ".."} for part in relative_path.split("/"))
                    or not relative_path.startswith("assets/screenshots/")
                    or candidate.as_posix() != relative_path):
                issues.append(f"approval manifest line {line_number}: unsafe image path")
                continue
            if relative_path in approved:
                issues.append(f"approval manifest line {line_number}: duplicate path {relative_path}")
            approved[relative_path] = digest.lower()
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        # A symlink inside the public tree must never cause a private file
        # outside the repository to be read or hashed by this gate.
        if path.is_symlink() and not path.resolve().is_relative_to(root.resolve()):
            issues.append(f"{relative}: symlink escapes public repository")
            continue
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            if relative not in approved:
                issues.append(f"{relative}: image lacks recorded publication approval")
            else:
                image_bytes = path.read_bytes()
                if len(image_bytes) > MAX_PUBLIC_IMAGE_BYTES:
                    issues.append(f"{relative}: image exceeds 8 MiB public size limit")
                if not image_format_matches(path, image_bytes):
                    issues.append(f"{relative}: image signature does not match its extension")
                for marker in embedded_metadata_markers(path, image_bytes):
                    issues.append(f"{relative}: embedded {marker} metadata requires removal and reapproval")
                if hashlib.sha256(image_bytes).hexdigest() != approved[relative]:
                    issues.append(f"{relative}: image bytes changed since publication approval")
        if path.suffix.lower() in WEB_EXTENSIONS:
            try:
                contents = path.read_text(encoding="utf-8")
            except UnicodeError:
                issues.append(f"{relative}: invalid UTF-8 public asset")
                continue
            for label in scan_text(contents):
                issues.append(f"{relative}: potential {label} in public asset")
            for label in scan_visual_embeds(contents, path.suffix.lower()):
                issues.append(f"{relative}: unapproved visual embed ({label})")
    for relative in approved:
        target = root / relative
        if (not target.is_file() or target.suffix.lower() not in IMAGE_EXTENSIONS
                or not target.resolve().is_relative_to(root.resolve())
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
