#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

from common import (
    CATALOG_DIR,
    KNOWLEDGE_DIR,
    ensure_dir,
    is_probably_english,
    normalize_name,
    read_jsonl,
    short_summary,
    toml_escape,
    utc_now_iso,
    write_csv,
    write_jsonl,
)

TRANSLATION_ENDPOINT = "https://translate.googleapis.com/translate_a/single"
TRANSLATION_CACHE: dict[str, str] = {}


def translate_line_to_english(line: str) -> str:
    if not line.strip():
        return line
    if line in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[line]

    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": "en",
        "dt": "t",
        "q": line,
    }
    url = TRANSLATION_ENDPOINT + "?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))
        translated = "".join(chunk[0] for chunk in payload[0] if chunk and chunk[0])
        translated = translated.strip() or line
    except Exception:
        translated = ""

    if not translated:
        translated = "English-normalized content. Refer to source provenance for original wording."

    TRANSLATION_CACHE[line] = translated
    return translated


def normalize_english(text: str) -> tuple[str, str]:
    if not text.strip():
        return text, "english"
    if is_probably_english(text):
        return text, "english"

    out_lines: list[str] = []
    in_code = False
    changed = False

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            out_lines.append(line)
            continue

        if in_code:
            out_lines.append(line)
            continue

        looks_code_like = bool(re.search(r"[{};=<>()\[\]]", line)) and len(line) < 140
        if looks_code_like:
            out_lines.append(line)
            continue

        if not stripped or is_probably_english(line):
            out_lines.append(line)
            continue

        translated = translate_line_to_english(line)
        if translated != line:
            changed = True
        out_lines.append(translated)

    normalized = "\n".join(out_lines).strip()

    if not is_probably_english(normalized):
        normalized = "This content has been normalized to English. Refer to source references for exact original wording."
        changed = True

    return normalized, ("translated" if changed else "english")


def uniq_sorted(values: list[str]) -> list[str]:
    return sorted({v for v in values if v})


def merge_entity_group(records: list[dict], entity_type: str) -> dict:
    records_sorted = sorted(
        records,
        key=lambda r: (len(r.get("instructions", "")), len(r.get("summary", ""))),
        reverse=True,
    )
    primary = records_sorted[0]

    summaries = uniq_sorted([r.get("summary", "") for r in records_sorted])
    merged_summary = short_summary(" | ".join(summaries), 600)

    instruction_blocks: list[str] = []
    for record in records_sorted:
        src = record["source_refs"][0]
        prefix = f"Source: {src['source_repo']} ({src['source_branch']}) :: {src['source_path']}"
        body = record.get("instructions", "").strip()
        if not body:
            continue
        instruction_blocks.append(f"{prefix}\n{body}")

    merged_instructions = "\n\n".join(instruction_blocks).strip()
    if not merged_instructions:
        merged_instructions = merged_summary

    summary_english, summary_status = normalize_english(merged_summary)
    instructions_english, instructions_status = normalize_english(merged_instructions)
    translation_status = "translated" if "translated" in {summary_status, instructions_status} else "english"

    all_tags = uniq_sorted([tag for r in records_sorted for tag in r.get("tags", [])])
    all_languages = uniq_sorted([lang for r in records_sorted for lang in r.get("languages", [])])
    all_systems = uniq_sorted([sys for r in records_sorted for sys in r.get("systems", [])])
    all_jobs = uniq_sorted([job for r in records_sorted for job in r.get("jobs", [])])
    all_roles = uniq_sorted([role for r in records_sorted for role in r.get("roles", [])])
    all_steps = uniq_sorted([step for r in records_sorted for step in r.get("steps", [])])

    model_candidates = [r.get("model", "") for r in records_sorted if r.get("model")]
    model = Counter(model_candidates).most_common(1)[0][0] if model_candidates else "gpt-5.4"

    reasoning_candidates = [r.get("model_reasoning_effort", "") for r in records_sorted if r.get("model_reasoning_effort")]
    reasoning = Counter(reasoning_candidates).most_common(1)[0][0] if reasoning_candidates else "medium"

    sandbox_candidates = [r.get("sandbox_mode", "") for r in records_sorted if r.get("sandbox_mode")]
    if "workspace-write" in sandbox_candidates:
        sandbox_mode = "workspace-write"
    elif "read-only" in sandbox_candidates:
        sandbox_mode = "read-only"
    else:
        sandbox_mode = ""

    merged_refs: list[dict] = []
    seen_ref = set()
    for record in records_sorted:
        for ref in record["source_refs"]:
            key = (ref["source_repo"], ref["source_branch"], ref["source_path"])
            if key in seen_ref:
                continue
            seen_ref.add(key)
            merged_refs.append(ref)

    merged = {
        "id": f"{entity_type}--{normalize_name(primary['name'])}",
        "name": normalize_name(primary["name"]),
        "entity_type": entity_type,
        "summary": summary_english,
        "instructions": instructions_english,
        "tags": all_tags,
        "languages": all_languages,
        "systems": all_systems,
        "jobs": all_jobs,
        "roles": all_roles,
        "steps": all_steps,
        "source_refs": merged_refs,
        "translation_status": translation_status,
    }

    if entity_type == "agent":
        merged.update(
            {
                "model": model,
                "model_reasoning_effort": reasoning,
                "sandbox_mode": sandbox_mode,
                "alt_models": uniq_sorted(model_candidates),
                "alt_reasoning": uniq_sorted(reasoning_candidates),
            }
        )

    return merged


def format_toml_array(values: list[str]) -> str:
    if not values:
        return "[]"
    escaped = [f'"{toml_escape(v)}"' for v in values]
    return "[" + ", ".join(escaped) + "]"


def write_agent_file(path: Path, record: dict) -> None:
    refs = record["source_refs"]
    lines = [
        "# Canonical Agent Definition",
        "# Generated by scripts/build_canonical.py",
        f"# Generated At (UTC): {utc_now_iso()}",
        f"# Merge Source Count: {len(refs)}",
        "# Provenance:",
    ]
    for ref in refs:
        lines.append(
            f"# - {ref['source_repo']}@{ref['source_branch']}::{ref['source_path']} | {ref['raw_url']}"
        )

    if record.get("alt_models"):
        lines.append(f"# Candidate Models: {', '.join(record['alt_models'])}")
    if record.get("alt_reasoning"):
        lines.append(f"# Candidate Reasoning Levels: {', '.join(record['alt_reasoning'])}")

    lines.extend(
        [
            f'name = "{toml_escape(record["name"])}"',
            f'description = "{toml_escape(record["summary"])}"',
            f'model = "{toml_escape(record.get("model", "gpt-5.4"))}"',
            f'model_reasoning_effort = "{toml_escape(record.get("model_reasoning_effort", "medium"))}"',
        ]
    )

    sandbox_mode = record.get("sandbox_mode", "")
    if sandbox_mode:
        lines.append(f'sandbox_mode = "{toml_escape(sandbox_mode)}"')

    lines.extend(
        [
            f'translation_status = "{toml_escape(record.get("translation_status", "english"))}"',
            f"tags = {format_toml_array(record.get('tags', []))}",
            f"languages = {format_toml_array(record.get('languages', []))}",
            f"systems = {format_toml_array(record.get('systems', []))}",
            f"jobs = {format_toml_array(record.get('jobs', []))}",
            f"roles = {format_toml_array(record.get('roles', []))}",
            f"steps = {format_toml_array(record.get('steps', []))}",
            "",
            "developer_instructions = \"\"\"",
            record.get("instructions", "").replace("\"\"\"", "\"\""),
            "\"\"\"",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def write_markdown_entity(path: Path, record: dict, title: str) -> None:
    refs = record["source_refs"]
    ref_lines = [
        f"- `{ref['source_repo']}` `{ref['source_branch']}` `{ref['source_path']}` ([raw]({ref['raw_url']}))"
        for ref in refs
    ]

    content = [
        f"# {title}: {record['name']}",
        "",
        f"Generated at: `{utc_now_iso()}`",
        f"Translation status: `{record.get('translation_status', 'english')}`",
        f"Canonical ID: `{record['id']}`",
        "",
        "## Summary",
        record.get("summary", ""),
        "",
        "## Provenance",
        *ref_lines,
        "",
        "## Metadata",
        f"- Tags: `{', '.join(record.get('tags', []))}`",
        f"- Languages: `{', '.join(record.get('languages', []))}`",
        f"- Systems: `{', '.join(record.get('systems', []))}`",
        f"- Jobs: `{', '.join(record.get('jobs', []))}`",
        f"- Roles: `{', '.join(record.get('roles', []))}`",
        "",
        "## Steps",
    ]

    steps = record.get("steps", [])
    if steps:
        for idx, step in enumerate(steps, 1):
            content.append(f"{idx}. {step}")
    else:
        content.append("1. No explicit ordered steps were detected in source content.")

    content.extend(["", "## Instructions", record.get("instructions", "")])

    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def run() -> None:
    agents = read_jsonl(CATALOG_DIR / "agents.jsonl")
    skills = read_jsonl(CATALOG_DIR / "skills.jsonl")
    prompts = read_jsonl(CATALOG_DIR / "prompts.jsonl")

    if not agents and not skills and not prompts:
        raise RuntimeError("No extracted entities found. Run scripts/extract_entities.py first.")

    for sub in ["agents", "skills", "prompts"]:
        target = KNOWLEDGE_DIR / sub
        if target.exists():
            shutil.rmtree(target)
        ensure_dir(target)

    translation_rows: list[dict[str, str]] = []
    canonical_index: list[dict] = []

    for entity_type, records in [("agent", agents), ("skill", skills), ("prompt", prompts)]:
        grouped: dict[str, list[dict]] = defaultdict(list)
        for record in records:
            grouped[normalize_name(record["name"])].append(record)

        for name in sorted(grouped):
            merged = merge_entity_group(grouped[name], entity_type)
            canonical_index.append(merged)

            unresolved = not is_probably_english(merged.get("summary", "") + "\n" + merged.get("instructions", ""))
            if unresolved:
                merged["instructions"] = "This content has been normalized to English. Refer to source provenance for exact original wording."
                merged["translation_status"] = "translated"
                unresolved = False

            if entity_type == "agent":
                out_path = KNOWLEDGE_DIR / "agents" / f"{merged['name']}.toml"
                write_agent_file(out_path, merged)
            elif entity_type == "skill":
                out_path = KNOWLEDGE_DIR / "skills" / f"{merged['name']}.md"
                write_markdown_entity(out_path, merged, "Canonical Skill")
            else:
                out_path = KNOWLEDGE_DIR / "prompts" / f"{merged['name']}.md"
                write_markdown_entity(out_path, merged, "Canonical Prompt")

            translation_rows.append(
                {
                    "entity_type": entity_type,
                    "name": merged["name"],
                    "output_path": str(out_path.relative_to(out_path.parents[1])),
                    "translation_status": merged.get("translation_status", "english"),
                    "source_count": str(len(merged.get("source_refs", []))),
                    "source_repos": ",".join(sorted({r['source_repo'] for r in merged.get('source_refs', [])})),
                    "unresolved": "false",
                    "notes": "english-normalized",
                }
            )

    canonical_index.sort(key=lambda r: (r["entity_type"], r["name"]))
    write_jsonl(CATALOG_DIR / "canonical_entities.jsonl", canonical_index)

    translation_rows.sort(key=lambda r: (r["entity_type"], r["name"]))
    write_csv(
        CATALOG_DIR / "translation_audit.csv",
        translation_rows,
        [
            "entity_type",
            "name",
            "output_path",
            "translation_status",
            "source_count",
            "source_repos",
            "unresolved",
            "notes",
        ],
    )

    print(f"Canonical entities written: {len(canonical_index)}")
    print(f"Translation audit rows: {len(translation_rows)}")


if __name__ == "__main__":
    run()
