#!/usr/bin/env python3
"""Build a Playwright handoff CSV with public demo URLs."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse


DEMO_PATH_FIELDS = [
    "relative_output_path",
    "demo_path",
    "output_path",
    "url(デモ)",
    "demo_url",
    "output_filename",
]


def is_http_url(value: str) -> bool:
    return bool(re.match(r"^https?://", str(value or "").strip(), flags=re.IGNORECASE))


def pick(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value and str(value).strip():
            return str(value).strip()
    return ""


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize_demo_path(raw_path: str, row: dict[str, str], strip_prefix: str, path_style: str = "preserve") -> str:
    value = str(raw_path or "").strip()
    if not value:
        return ""

    if is_http_url(value):
        parsed_path = urlparse(value).path.lstrip("/")
        value = parsed_path or Path(urlparse(value).path).name

    value = value.replace("\\", "/").split("?", 1)[0].split("#", 1)[0].strip()
    while value.startswith("./"):
        value = value[2:]

    marker = f"/{strip_prefix.strip('/')}/"
    if marker in value:
        value = value.split(marker, 1)[1]

    prefix = strip_prefix.strip("/")
    if prefix and value.startswith(prefix + "/"):
        value = value[len(prefix) + 1 :]

    value = value.lstrip("/")
    if "/" not in value:
        template = pick(row, "template").strip().strip("/")
        if template:
            value = f"{template}/{value}"
    value = "/".join(part.lower() for part in value.split("/"))
    if path_style == "basename":
        return value.rsplit("/", 1)[-1]
    return value


def build_public_url(base_url: str, path_value: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", path_value.lstrip("/"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fill demo_url/url(デモ) with public URLs while preserving handoff fields."
    )
    parser.add_argument("--input", required=True, help="Existing handoff_with_demo_paths.csv")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--demo-url-base", required=True, help="Public base URL for deployed demos")
    parser.add_argument(
        "--strip-prefix",
        default="output",
        help="Local path prefix to strip before appending to --demo-url-base.",
    )
    parser.add_argument(
        "--path-style",
        choices=["preserve", "basename"],
        default="preserve",
        help="Use 'basename' when deployed demos live at the public site root instead of template subfolders.",
    )
    args = parser.parse_args()

    base_url = str(args.demo_url_base or "").strip()
    if not is_http_url(base_url):
        raise SystemExit("--demo-url-base must start with http:// or https://")

    input_path = Path(args.input)
    output_path = Path(args.output)
    rows, fieldnames = read_rows(input_path)
    if not rows:
        raise SystemExit(f"No rows found in {input_path}")

    for field in ["demo_url", "url(デモ)"]:
        if field not in fieldnames:
            fieldnames.append(field)

    filled = 0
    missing = 0
    for row in rows:
        raw_path = pick(row, *DEMO_PATH_FIELDS)
        public_path = normalize_demo_path(raw_path, row, args.strip_prefix, args.path_style)
        if not public_path:
            missing += 1
            continue
        public_url = build_public_url(base_url, public_path)
        row["demo_url"] = public_url
        row["url(デモ)"] = public_url
        filled += 1

    write_rows(output_path, fieldnames, rows)
    print(f"input={input_path}")
    print(f"output={output_path}")
    print(f"rows={len(rows)}")
    print(f"public_demo_url_filled={filled}")
    print(f"public_demo_url_missing={missing}")
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
