#!/usr/bin/env python3
"""Build a public-safe deploy folder from referenced demo HTML/assets."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


HTML_FIELDS = [
    "relative_output_path",
    "demo_path",
    "output_path",
    "output_filename",
]

PUBLIC_SAFE_EXTENSIONS = {
    ".html",
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
ASSET_EXTENSIONS = PUBLIC_SAFE_EXTENSIONS
REFERENCE_SCAN_EXTENSIONS = {".css", ".html"}
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
    "metadata",
    "review_queue",
    "submission",
    "cooldown",
    "blocklist",
    "screenshot",
    "state",
}
SKIPPED_SCHEMES = {
    "data",
    "javascript",
    "mailto",
    "sms",
    "tel",
}
CSS_URL_RE = re.compile(
    r"""url\(\s*(?P<quote>['"]?)(?P<url>.*?)(?P=quote)\s*\)""",
    flags=re.IGNORECASE,
)


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
    if path.suffix.lower() in FORBIDDEN_EXTENSIONS:
        return True
    path_parts = [part.lower() for part in path.parts]
    return any(forbidden in part for part in path_parts for forbidden in FORBIDDEN_NAME_PARTS)


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

    raw_path = Path(value)
    if raw_path.is_absolute():
        candidate = raw_path.resolve()
        try:
            candidate.relative_to(source_root.resolve())
        except ValueError:
            return None
        return candidate

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
    public_relative = Path(*[part.lower() for part in relative.parts])
    return deploy_root / public_relative


def copy_file(source_path: Path, source_root: Path, deploy_root: Path, copied: set[Path]) -> Path | None:
    if not source_path.exists() or not source_path.is_file():
        return None
    if source_path.suffix.lower() not in PUBLIC_SAFE_EXTENSIONS:
        return None
    if is_forbidden_public_file(source_path):
        return None
    dest = destination_for(source_path, source_root, deploy_root)
    if dest in copied:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, dest)
    copied.add(dest)
    return dest


def css_url_refs(text: str) -> list[str]:
    refs: list[str] = []
    for match in CSS_URL_RE.finditer(text):
        ref = match.group("url").strip()
        if ref:
            refs.append(ref)
    return refs


def split_srcset(value: str) -> list[str]:
    refs: list[str] = []
    for candidate in value.split(","):
        ref = candidate.strip().split(None, 1)[0].strip()
        if ref:
            refs.append(ref)
    return refs


class HtmlAssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._collect_attrs(attrs)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._collect_attrs(attrs)

    def _collect_attrs(self, attrs: list[tuple[str, str | None]]) -> None:
        for raw_name, raw_value in attrs:
            if not raw_name or raw_value is None:
                continue
            name = raw_name.lower()
            value = raw_value.strip()
            if not value:
                continue
            if name in {"href", "src"}:
                self.refs.append(value)
            elif name in {"srcset", "imagesrcset"}:
                self.refs.extend(split_srcset(value))
            elif name == "style":
                self.refs.extend(css_url_refs(value))


def extract_html_refs(html: str) -> list[str]:
    parser = HtmlAssetParser()
    parser.feed(html)
    parser.close()
    return parser.refs + css_url_refs(html)


def normalize_local_ref(ref: str, base_path: Path, source_root: Path) -> Path | None:
    value = unescape(str(ref or "").strip())
    if not value or value.startswith("#"):
        return None
    parsed = urlparse(value)
    if parsed.scheme in SKIPPED_SCHEMES or parsed.scheme in {"http", "https"} or parsed.netloc:
        return None
    rel = unquote(parsed.path).replace("\\", "/").strip()
    if not rel:
        return None
    if Path(rel).suffix.lower() not in ASSET_EXTENSIONS:
        return None
    if rel.startswith("/"):
        candidate = (source_root / rel.lstrip("/")).resolve()
    else:
        candidate = (base_path.parent / rel).resolve()
    try:
        candidate.relative_to(source_root.resolve())
    except ValueError:
        return None
    return candidate


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def referenced_assets(html_path: Path, source_root: Path) -> list[Path]:
    try:
        text = html_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = html_path.read_text(encoding="utf-8-sig")

    suffix = html_path.suffix.lower()
    if suffix == ".html":
        refs = extract_html_refs(text)
    elif suffix == ".css":
        refs = css_url_refs(text)
    else:
        refs = []

    assets: list[Path] = []
    for ref in refs:
        candidate = normalize_local_ref(ref, html_path, source_root)
        if candidate:
            assets.append(candidate)
    return unique_paths(assets)


def copy_referenced_assets(
    initial_assets: list[Path],
    source_root: Path,
    deploy_root: Path,
    copied: set[Path],
    scanned_reference_files: set[Path],
) -> tuple[list[Path], list[Path], list[Path]]:
    queue = list(initial_assets)
    queued = set(queue)
    copied_assets: list[Path] = []
    missing_assets: list[Path] = []
    skipped_assets: list[Path] = []

    while queue:
        asset_path = queue.pop(0)
        if not asset_path.exists() or not asset_path.is_file():
            missing_assets.append(asset_path)
            continue
        if asset_path.suffix.lower() not in PUBLIC_SAFE_EXTENSIONS or is_forbidden_public_file(asset_path):
            skipped_assets.append(asset_path)
            continue

        dest = copy_file(asset_path, source_root, deploy_root, copied)
        if dest:
            copied_assets.append(dest)

        if asset_path.suffix.lower() not in REFERENCE_SCAN_EXTENSIONS:
            continue
        if asset_path in scanned_reference_files:
            continue
        scanned_reference_files.add(asset_path)
        for nested_asset in referenced_assets(asset_path, source_root):
            if nested_asset in queued:
                continue
            queued.add(nested_asset)
            queue.append(nested_asset)

    return copied_assets, unique_paths(missing_assets), unique_paths(skipped_assets)


def missing_references(entry_paths: list[Path], root: Path) -> list[Path]:
    queue = list(entry_paths)
    queued = set(queue)
    scanned: set[Path] = set()
    missing: list[Path] = []

    while queue:
        current = queue.pop(0)
        if current in scanned or not current.exists() or not current.is_file():
            continue
        scanned.add(current)
        for asset_path in referenced_assets(current, root):
            if not asset_path.exists() or not asset_path.is_file():
                missing.append(asset_path)
                continue
            if asset_path.suffix.lower() in REFERENCE_SCAN_EXTENSIONS and asset_path not in queued:
                queued.add(asset_path)
                queue.append(asset_path)
    return unique_paths(missing)


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
    scanned_reference_files: set[Path] = set()
    missing_html: list[str] = []
    copied_html_paths: list[Path] = []
    copied_asset_paths: list[Path] = []
    source_missing_assets: list[Path] = []
    skipped_assets: list[Path] = []

    for row in rows:
        raw_html = pick(row, *HTML_FIELDS)
        html_path = resolve_source_path(raw_html, row, source_root, args.strip_prefix)
        if not html_path or html_path.suffix.lower() != ".html" or not html_path.exists():
            missing_html.append(raw_html)
            continue
        html_dest = copy_file(html_path, source_root, deploy_root, copied)
        if html_dest:
            copied_html_paths.append(html_dest)
        scanned_reference_files.add(html_path)
        asset_copies, asset_missing, asset_skipped = copy_referenced_assets(
            referenced_assets(html_path, source_root),
            source_root,
            deploy_root,
            copied,
            scanned_reference_files,
        )
        copied_asset_paths.extend(asset_copies)
        source_missing_assets.extend(asset_missing)
        skipped_assets.extend(asset_skipped)

    forbidden = scan_forbidden_outputs(deploy_root)
    html_files = sorted(path for path in deploy_root.rglob("*.html") if path.is_file())
    deploy_missing_assets = missing_references(html_files, deploy_root)
    source_missing_assets = unique_paths(source_missing_assets)
    skipped_assets = unique_paths(skipped_assets)
    copied_asset_relpaths = [
        str(path.resolve().relative_to(deploy_root)) for path in copied_asset_paths if path.suffix.lower() != ".html"
    ]

    print(f"input={input_path}")
    print(f"output_dir={deploy_root}")
    print(f"rows={len(rows)}")
    print(f"html_copied={len(copied_html_paths)}")
    print(f"html_count={len(html_files)}")
    print(f"asset_files_copied={len(copied_asset_paths)}")
    print(f"missing_html={len(missing_html)}")
    print(f"source_missing_assets={len(source_missing_assets)}")
    print(f"skipped_assets={len(skipped_assets)}")
    print(f"missing_assets={len(deploy_missing_assets)}")
    print(f"forbidden_files={len(forbidden)}")
    print("copied_asset_paths_first20=")
    for relpath in copied_asset_relpaths[:20]:
        print(f"  {relpath}")
    if missing_html:
        print("missing_html_examples=" + ",".join(missing_html[:5]))
    if source_missing_assets:
        print("source_missing_asset_examples=" + ",".join(str(path) for path in source_missing_assets[:5]))
    if skipped_assets:
        print("skipped_asset_examples=" + ",".join(str(path) for path in skipped_assets[:5]))
    if deploy_missing_assets:
        print("missing_asset_examples=" + ",".join(str(path) for path in deploy_missing_assets[:5]))
    if forbidden:
        print("forbidden_examples=" + ",".join(str(path) for path in forbidden[:5]))
    return 0 if not missing_html and not source_missing_assets and not skipped_assets and not deploy_missing_assets and not forbidden else 1


if __name__ == "__main__":
    raise SystemExit(main())
