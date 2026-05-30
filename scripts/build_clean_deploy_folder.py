#!/usr/bin/env python3
"""Build a public-safe deploy folder from referenced demo HTML/assets."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlparse


HTML_FIELDS = [
    "relative_output_path",
    "demo_path",
    "output_path",
    "output_filename",
]

ASSET_EXTENSIONS = {
    ".css",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".png",
    ".svg",
    ".webp",
    ".woff",
    ".woff2",
}
FORBIDDEN_EXTENSIONS = {
    ".csv",
    ".json",
    ".jsonl",
    ".log",
    ".md",
    ".txt",
    ".xlsx",
    ".xls",
}
FORBIDDEN_NAME_PARTS = {
    "handoff",
    "ledger",
    "review_queue",
    "submission",
    "cooldown",
    "blocklist",
    "screenshot",
    "state",
}


def pick(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value and str(value).strip():
            return str(value).strip()
    return ""


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def clean_output_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def is_forbidden_public_file(path: Path) -> bool:
    name = path.name.lower()
    if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
        return True
    return any(part in name for part in FORBIDDEN_NAME_PARTS)


def resolve_source_path(raw_value: str, row: dict[str, str], source_root: Path, strip_prefix: str) -> Path | None:
    value = str(raw_value or "").strip()
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"}:
        value = unquote(parsed.path.lstrip("/"))
    value = value.replace("\\", "/").split("?", 1)[0].split("#", 1)[0].strip()
    while value.startswith("./"):
        value = value[2:]

    prefix = strip_prefix.strip("/")
    marker = f"/{prefix}/" if prefix else ""
    if marker and marker in value:
        value = value.split(marker, 1)[1]
    if prefix and value.startswith(prefix + "/"):
        value = value[len(prefix) + 1 :]

    value = value.lstrip("/")
    if "/" not in value:
        template = pick(row, "template").strip().strip("/")
        if template:
            value = f"{template}/{value}"

    candidate = (source_root / value).resolve()
    try:
        candidate.relative_to(source_root.resolve())
    except ValueError:
        return None
    return candidate


def destination_for(source_path: Path, source_root: Path, deploy_root: Path) -> Path:
    relative = source_path.resolve().relative_to(source_root.resolve())
    return deploy_root / relative


def copy_file(source_path: Path, source_root: Path, deploy_root: Path, copied: set[Path]) -> bool:
    if not source_path.exists() or not source_path.is_file():
        return False
    if is_forbidden_public_file(source_path):
        return False
    dest = destination_for(source_path, source_root, deploy_root)
    if dest in copied:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, dest)
    copied.add(dest)
    return True


def referenced_assets(html_path: Path, source_root: Path) -> list[Path]:
    try:
        html = html_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        html = html_path.read_text(encoding="utf-8-sig")

    refs = re.findall(r"""(?:src|href)=["']([^"']+)["']""", html, flags=re.IGNORECASE)
    assets: list[Path] = []
    for ref in refs:
        ref = ref.strip()
        if not ref or ref.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
            continue
        parsed = urlparse(ref)
        if parsed.scheme in {"http", "https"} or parsed.netloc:
            continue
        rel = unquote(parsed.path)
        if not rel or Path(rel).suffix.lower() not in ASSET_EXTENSIONS:
            continue
        candidate = (html_path.parent / rel).resolve()
        try:
            candidate.relative_to(source_root.resolve())
        except ValueError:
            continue
        assets.append(candidate)
    return assets


def scan_forbidden_outputs(deploy_root: Path) -> list[Path]:
    bad: list[Path] = []
    for path in deploy_root.rglob("*"):
        if path.is_file() and is_forbidden_public_file(path):
            bad.append(path)
    return bad


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy only handoff-referenced public demo HTML/assets into deploy_public."
    )
    parser.add_argument("--input", default="output/handoff_with_demo_paths.csv", help="Handoff CSV")
    parser.add_argument("--output-dir", default="deploy_public", help="Clean deploy folder")
    parser.add_argument("--source-root", default="output", help="Generated output root")
    parser.add_argument("--strip-prefix", default="output", help="Prefix to strip from handoff paths")
    args = parser.parse_args()

    input_path = Path(args.input)
    source_root = Path(args.source_root).resolve()
    deploy_root = Path(args.output_dir).resolve()
    rows = read_rows(input_path)
    if not rows:
        raise SystemExit(f"No rows found in {input_path}")

    clean_output_dir(deploy_root)
    copied: set[Path] = set()
    missing_html: list[str] = []
    copied_html = 0
    copied_assets = 0

    for row in rows:
        raw_html = pick(row, *HTML_FIELDS)
        html_path = resolve_source_path(raw_html, row, source_root, args.strip_prefix)
        if not html_path or html_path.suffix.lower() != ".html" or not html_path.exists():
            missing_html.append(raw_html)
            continue
        if copy_file(html_path, source_root, deploy_root, copied):
            copied_html += 1
        for asset_path in referenced_assets(html_path, source_root):
            if copy_file(asset_path, source_root, deploy_root, copied):
                copied_assets += 1

    forbidden = scan_forbidden_outputs(deploy_root)
    print(f"input={input_path}")
    print(f"output_dir={deploy_root}")
    print(f"rows={len(rows)}")
    print(f"html_copied={copied_html}")
    print(f"asset_copy_events={copied_assets}")
    print(f"missing_html={len(missing_html)}")
    print(f"forbidden_files={len(forbidden)}")
    if missing_html:
        print("missing_html_examples=" + ",".join(missing_html[:5]))
    if forbidden:
        print("forbidden_examples=" + ",".join(str(path) for path in forbidden[:5]))
    return 0 if not missing_html and not forbidden else 1


if __name__ == "__main__":
    raise SystemExit(main())
