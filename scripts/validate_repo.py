#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from common import CATALOG_DIR, KNOWLEDGE_DIR, REPO_ROOT, SOURCES_DIR, load_sources, read_jsonl, source_slug


class ValidationError(Exception):
    pass


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValidationError(f"Missing required CSV: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_source_coverage() -> None:
    source_rows = read_csv_rows(CATALOG_DIR / "source_files.csv")
    indexed_set = {
        (r["source_repo"], r["source_branch"], r["source_path"]) for r in source_rows
    }

    actual_set = set()
    for source in load_sources():
        root = SOURCES_DIR / source_slug(source)
        if not root.exists():
            raise ValidationError(f"Missing extracted source directory: {root}")
        repo_id = f"{source['owner']}/{source['repo']}"
        branch = source["branch"]
        for file_path in root.rglob("*"):
            if file_path.is_file():
                rel = file_path.relative_to(root).as_posix()
                actual_set.add((repo_id, branch, rel))

    missing = actual_set - indexed_set
    extra = indexed_set - actual_set

    if missing:
        sample = sorted(missing)[:5]
        raise ValidationError(f"Missing indexed files: {sample}")
    if extra:
        sample = sorted(extra)[:5]
        raise ValidationError(f"Indexed files not found in source tree: {sample}")


def validate_binary_index() -> None:
    source_rows = read_csv_rows(CATALOG_DIR / "source_files.csv")
    binary_rows = read_csv_rows(CATALOG_DIR / "binary_assets.csv")

    source_binary = {
        (r["source_repo"], r["source_branch"], r["source_path"]) for r in source_rows if r["classification"] == "binary"
    }
    binary_index = {
        (r["source_repo"], r["source_branch"], r["source_path"]) for r in binary_rows
    }

    if source_binary != binary_index:
        diff_a = sorted(source_binary - binary_index)[:5]
        diff_b = sorted(binary_index - source_binary)[:5]
        raise ValidationError(
            f"Binary index mismatch. Missing in binary_assets: {diff_a}; extra in binary_assets: {diff_b}"
        )


def validate_canonical_uniqueness() -> None:
    agent_files = sorted((KNOWLEDGE_DIR / "agents").glob("*.toml"))
    names = [f.stem for f in agent_files]
    if len(names) != len(set(names)):
        raise ValidationError("Duplicate canonical agent filenames detected.")


def validate_translation_audit() -> None:
    rows = read_csv_rows(CATALOG_DIR / "translation_audit.csv")
    unresolved = [r for r in rows if r.get("unresolved", "").strip().lower() == "true"]
    if unresolved:
        raise ValidationError(f"Found unresolved translation rows: {len(unresolved)}")


def validate_source_refs() -> None:
    records = read_jsonl(CATALOG_DIR / "canonical_entities.jsonl")
    bad = [r["id"] for r in records if not r.get("source_refs")]
    if bad:
        raise ValidationError(f"Canonical entities missing source_refs: {bad[:10]}")


def validate_links(path: Path) -> None:
    if not path.exists():
        raise ValidationError(f"Missing markdown file: {path}")

    content = path.read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
    local_links = [link for link in links if not re.match(r"^[a-zA-Z]+://", link)]

    for link in local_links:
        file_part = link.split("#", 1)[0]
        if not file_part:
            continue
        target = (path.parent / file_part).resolve()
        if not target.exists():
            raise ValidationError(f"Broken local link in {path}: {link}")


def run() -> None:
    checks = [
        ("source coverage", validate_source_coverage),
        ("binary index", validate_binary_index),
        ("canonical uniqueness", validate_canonical_uniqueness),
        ("translation audit", validate_translation_audit),
        ("source refs", validate_source_refs),
        ("README links", lambda: validate_links(REPO_ROOT / "README.md")),
        ("Obsidian links", lambda: validate_links(REPO_ROOT / "Obsidian-Helper.md")),
    ]

    failures: list[str] = []
    for name, fn in checks:
        try:
            fn()
            print(f"[OK] {name}")
        except Exception as exc:
            failures.append(f"[FAIL] {name}: {exc}")

    if failures:
        print("\n".join(failures))
        raise SystemExit(1)

    print("Validation completed successfully")


if __name__ == "__main__":
    run()
