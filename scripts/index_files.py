#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from common import (
    CATALOG_DIR,
    SOURCES_DIR,
    classify_bytes,
    ensure_dir,
    file_ext,
    guess_asset_purpose,
    load_sources,
    raw_file_url,
    sha256_bytes,
    source_repo_id,
    source_slug,
    write_csv,
)


def run() -> None:
    ensure_dir(CATALOG_DIR)

    source_rows: list[dict[str, str]] = []
    binary_rows: list[dict[str, str]] = []

    for source in load_sources():
        slug = source_slug(source)
        root = SOURCES_DIR / slug
        if not root.exists():
            raise FileNotFoundError(
                f"Missing extracted source directory: {root}. Run scripts/fetch_sources.py first."
            )

        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rel = path.relative_to(root).as_posix()
            data = path.read_bytes()
            classification = classify_bytes(rel, data)
            ext = file_ext(rel)
            row = {
                "source_repo": source_repo_id(source),
                "source_branch": source["branch"],
                "source_path": rel,
                "ext": ext,
                "size_bytes": str(len(data)),
                "sha256": sha256_bytes(data),
                "raw_url": raw_file_url(source, rel),
                "classification": classification,
            }
            source_rows.append(row)

            if classification == "binary":
                binary_rows.append(
                    {
                        "source_repo": row["source_repo"],
                        "source_branch": row["source_branch"],
                        "source_path": row["source_path"],
                        "ext": row["ext"],
                        "size_bytes": row["size_bytes"],
                        "sha256": row["sha256"],
                        "raw_url": row["raw_url"],
                        "purpose": guess_asset_purpose(rel),
                    }
                )

    source_rows.sort(key=lambda r: (r["source_repo"], r["source_path"]))
    binary_rows.sort(key=lambda r: (r["source_repo"], r["source_path"]))

    write_csv(
        CATALOG_DIR / "source_files.csv",
        source_rows,
        [
            "source_repo",
            "source_branch",
            "source_path",
            "ext",
            "size_bytes",
            "sha256",
            "raw_url",
            "classification",
        ],
    )

    write_csv(
        CATALOG_DIR / "binary_assets.csv",
        binary_rows,
        [
            "source_repo",
            "source_branch",
            "source_path",
            "ext",
            "size_bytes",
            "sha256",
            "raw_url",
            "purpose",
        ],
    )

    print(f"Indexed {len(source_rows)} files")
    print(f"Indexed {len(binary_rows)} binary assets")


if __name__ == "__main__":
    run()
