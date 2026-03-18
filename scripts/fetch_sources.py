#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

from common import (
    CATALOG_DIR,
    RAW_DIR,
    SOURCES_DIR,
    codeload_url,
    ensure_dir,
    load_sources,
    sha256_file,
    source_repo_id,
    source_slug,
    utc_now_iso,
)


def download_archive(url: str, dest: Path) -> None:
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()
    dest.write_bytes(data)


def extract_archive(archive_path: Path, target_dir: Path) -> None:
    if target_dir.exists():
        shutil.rmtree(target_dir)

    ensure_dir(target_dir.parent)
    temp_dir = Path(tempfile.mkdtemp(prefix="codex_extract_"))
    try:
        with tarfile.open(archive_path, mode="r:gz") as tar:
            tar.extractall(temp_dir)

        roots = [p for p in temp_dir.iterdir() if p.is_dir()]
        if len(roots) == 1:
            shutil.move(str(roots[0]), str(target_dir))
        else:
            ensure_dir(target_dir)
            for item in temp_dir.iterdir():
                shutil.move(str(item), str(target_dir / item.name))
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def run(refresh: bool) -> None:
    ensure_dir(RAW_DIR)
    ensure_dir(SOURCES_DIR)
    ensure_dir(CATALOG_DIR)

    rows: list[dict[str, str]] = []
    for source in load_sources():
        slug = source_slug(source)
        archive_path = RAW_DIR / f"{slug}.tar.gz"
        extract_path = SOURCES_DIR / slug

        if refresh or not archive_path.exists():
            print(f"Downloading {source_repo_id(source)}@{source['branch']} ...")
            download_archive(codeload_url(source), archive_path)
        else:
            print(f"Using cached archive {archive_path.name}")

        print(f"Extracting {archive_path.name} ...")
        extract_archive(archive_path, extract_path)

        rows.append(
            {
                "source_repo": source_repo_id(source),
                "source_branch": source["branch"],
                "archive_path": str(archive_path.relative_to(archive_path.parents[1])),
                "archive_size_bytes": str(archive_path.stat().st_size),
                "archive_sha256": sha256_file(archive_path),
                "downloaded_at_utc": utc_now_iso(),
            }
        )

    rows.sort(key=lambda r: (r["source_repo"], r["source_branch"]))
    out_path = CATALOG_DIR / "source_archives.csv"
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_repo",
                "source_branch",
                "archive_path",
                "archive_size_bytes",
                "archive_sha256",
                "downloaded_at_utc",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and extract all configured source repositories.")
    parser.add_argument("--refresh", action="store_true", help="Force re-download of source archives.")
    args = parser.parse_args()
    run(refresh=args.refresh)


if __name__ == "__main__":
    main()
