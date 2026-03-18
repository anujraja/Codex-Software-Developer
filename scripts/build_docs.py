#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from common import (
    CATALOG_DIR,
    DOCS_DIR,
    KNOWLEDGE_DIR,
    REPO_ROOT,
    load_sources,
    read_jsonl,
    utc_now_iso,
)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_source_map(
    source_files: list[dict[str, str]],
    binary_assets: list[dict[str, str]],
    agents: list[dict],
    skills: list[dict],
    prompts: list[dict],
) -> str:
    files_by_repo = Counter(row["source_repo"] for row in source_files)
    binaries_by_repo = Counter(row["source_repo"] for row in binary_assets)

    extracted_counts: dict[str, Counter] = defaultdict(Counter)
    for collection_name, records in (("agents", agents), ("skills", skills), ("prompts", prompts)):
        for record in records:
            for ref in record.get("source_refs", []):
                extracted_counts[ref["source_repo"]][collection_name] += 1

    lines = [
        "# Source Map",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "| Source Repo | Branch | Total Files | Binary Assets | Agent Records | Skill Records | Prompt Records |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for source in load_sources():
        repo = f"{source['owner']}/{source['repo']}"
        lines.append(
            "| "
            + " | ".join(
                [
                    repo,
                    source["branch"],
                    str(files_by_repo.get(repo, 0)),
                    str(binaries_by_repo.get(repo, 0)),
                    str(extracted_counts[repo].get("agents", 0)),
                    str(extracted_counts[repo].get("skills", 0)),
                    str(extracted_counts[repo].get("prompts", 0)),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "- All source files are indexed in `catalog/source_files.csv`.",
            "- Binary assets are indexed (not copied) in `catalog/binary_assets.csv`.",
            "- Canonical merged outputs are generated under `knowledge/`.",
        ]
    )

    return "\n".join(lines)


def build_merge_policy() -> str:
    return "\n".join(
        [
            "# Merge Policy",
            "",
            f"Generated at: `{utc_now_iso()}`",
            "",
            "## Canonicalization Rules",
            "1. Source inputs are parsed into normalized entity contracts in `catalog/*.jsonl`.",
            "2. For duplicate agent names, one canonical file is generated per normalized name.",
            "3. Canonical agent files preserve explicit provenance comments for every source reference.",
            "4. Skills and prompts are generated as canonical Markdown knowledge entries with provenance sections.",
            "5. Binary files are not copied; they remain indexed by URL and hash in `catalog/binary_assets.csv`.",
            "",
            "## Translation Rules",
            "1. Canonical outputs must be English-first.",
            "2. Non-English text is auto-normalized to English during canonical build.",
            "3. Translation outcomes are tracked in `catalog/translation_audit.csv`.",
            "",
            "## Determinism",
            "- Sorting is stable for all entity lists and output paths.",
            "- Regeneration may change timestamps, but logical content and counts remain stable.",
        ]
    )


def build_matrix(taxonomy: dict) -> str:
    roles = taxonomy.get("roles", [])[:30]
    languages = taxonomy.get("languages", [])[:30]
    systems = taxonomy.get("systems", [])[:30]

    lines = [
        "# Agent/Role/Language/System Matrix",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Top Roles",
        "| Role | Count |",
        "|---|---:|",
    ]
    for row in roles:
        lines.append(f"| {row['name']} | {row['count']} |")

    lines.extend(["", "## Top Languages", "| Language | Count |", "|---|---:|"])
    for row in languages:
        lines.append(f"| {row['name']} | {row['count']} |")

    lines.extend(["", "## Top Systems", "| System | Count |", "|---|---:|"])
    for row in systems:
        lines.append(f"| {row['name']} | {row['count']} |")

    return "\n".join(lines)


def build_prompt_library(prompts: list[dict]) -> str:
    lines = [
        "# Prompt Library",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "| Prompt | Summary | Source Count |",
        "|---|---|---:|",
    ]

    for record in sorted(prompts, key=lambda r: r["name"]):
        summary = " ".join(record.get("summary", "").split())
        summary = summary[:180] + "..." if len(summary) > 180 else summary
        lines.append(
            f"| `{record['name']}` | {summary} | {len(record.get('source_refs', []))} |"
        )

    lines.extend(
        [
            "",
            "Each canonical prompt file is available under `knowledge/prompts/`.",
        ]
    )

    return "\n".join(lines)


def build_developer_guide() -> str:
    return "\n".join(
        [
            "# Developer Guide",
            "",
            f"Generated at: `{utc_now_iso()}`",
            "",
            "## Pipeline Commands",
            "```bash",
            "python3 scripts/fetch_sources.py",
            "python3 scripts/index_files.py",
            "python3 scripts/extract_entities.py",
            "python3 scripts/build_canonical.py",
            "python3 scripts/build_docs.py",
            "python3 scripts/validate_repo.py",
            "```",
            "",
            "## Update Workflow",
            "1. Update `config/sources.yaml` when adding/removing source repositories.",
            "2. Run the full pipeline in order.",
            "3. Review `catalog/duplicates_agents.json` for merge impacts.",
            "4. Confirm `catalog/translation_audit.csv` has no unresolved rows.",
            "5. Run validation and commit generated outputs.",
            "",
            "## Key Outputs",
            "- `catalog/source_files.csv` full source file manifest",
            "- `catalog/binary_assets.csv` binary asset index",
            "- `catalog/canonical_entities.jsonl` canonical unified entities",
            "- `knowledge/agents/*.toml` canonical merged agent definitions",
            "- `knowledge/skills/*.md` canonical skill documents",
            "- `knowledge/prompts/*.md` canonical prompt documents",
        ]
    )


def build_readme(
    source_files: list[dict[str, str]],
    binary_assets: list[dict[str, str]],
    canonical: list[dict],
    duplicates: dict,
    taxonomy: dict,
) -> str:
    entity_counter = Counter(r["entity_type"] for r in canonical)
    repo_list = [f"- `{s['owner']}/{s['repo']}` (`{s['branch']}`)" for s in load_sources()]

    top_roles = ", ".join(r["name"] for r in taxonomy.get("roles", [])[:8])
    top_languages = ", ".join(r["name"] for r in taxonomy.get("languages", [])[:8])

    return "\n".join(
        [
            "# Codex-Software-Developer",
            "",
            "Canonical, English-first, reproducible knowledge base for Codex agents, subagents, skills, roles, jobs, systems, prompts, and workflows.",
            "",
            "## What This Repo Does",
            "- Aggregates multiple public agent/skill repositories into one canonical index.",
            "- Deduplicates agent names and generates one merged canonical definition per name.",
            "- Preserves detailed provenance for every canonical output file.",
            "- Builds Obsidian-friendly docs and relationship maps.",
            "",
            "## Source Repositories",
            *repo_list,
            "",
            "## Current Snapshot",
            f"- Indexed source files: **{len(source_files)}**",
            f"- Indexed binary assets: **{len(binary_assets)}** (indexed only, not copied)",
            f"- Canonical agents: **{entity_counter.get('agent', 0)}**",
            f"- Canonical skills: **{entity_counter.get('skill', 0)}**",
            f"- Canonical prompts: **{entity_counter.get('prompt', 0)}**",
            f"- Cross-repo duplicate agent names merged: **{duplicates.get('total_duplicate_names', 0)}**",
            "",
            "## Taxonomy Highlights",
            f"- Top roles: {top_roles or 'n/a'}",
            f"- Top languages: {top_languages or 'n/a'}",
            "",
            "## Repository Layout",
            "```text",
            "config/                 # source definitions",
            "scripts/                # reproducible build/index/validate pipeline",
            "catalog/                # machine-readable manifests and normalized contracts",
            "knowledge/agents/       # canonical merged agent TOMLs",
            "knowledge/skills/       # canonical skill markdown",
            "knowledge/prompts/      # canonical prompt markdown",
            "docs/                   # source map, merge policy, matrix, guide",
            "Obsidian-Helper.md      # vault-first relationship guide",
            "```",
            "",
            "## Quickstart",
            "```bash",
            "python3 scripts/fetch_sources.py",
            "python3 scripts/index_files.py",
            "python3 scripts/extract_entities.py",
            "python3 scripts/build_canonical.py",
            "python3 scripts/build_docs.py",
            "python3 scripts/validate_repo.py",
            "```",
            "",
            "## Key Contracts",
            "Every canonical entity follows this schema:",
            "- `id`, `name`, `entity_type`, `summary`, `instructions`, `tags`,",
            "- `languages`, `systems`, `jobs`, `roles`, `steps`, `source_refs[]`, `translation_status`",
            "",
            "## Detailed Docs",
            "- [Source Map](docs/source-map.md)",
            "- [Merge Policy](docs/merge-policy.md)",
            "- [Agent Role Language System Matrix](docs/agent-role-language-system-matrix.md)",
            "- [Prompt Library](docs/prompt-library.md)",
            "- [Developer Guide](docs/developer-guide.md)",
            "- [Obsidian Helper](Obsidian-Helper.md)",
        ]
    )


def build_obsidian_helper(canonical: list[dict]) -> str:
    grouped = defaultdict(list)
    for record in canonical:
        grouped[record["entity_type"]].append(record)

    lines = [
        "# Obsidian-Helper",
        "",
        "Primary relationship map for using this repository inside an Obsidian vault.",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Folder Graph",
        "```mermaid",
        "graph TD",
        "  A[README.md] --> B[docs/source-map.md]",
        "  A --> C[docs/merge-policy.md]",
        "  A --> D[docs/agent-role-language-system-matrix.md]",
        "  A --> E[docs/prompt-library.md]",
        "  A --> F[docs/developer-guide.md]",
        "  A --> G[catalog/canonical_entities.jsonl]",
        "  G --> H[knowledge/agents/]",
        "  G --> I[knowledge/skills/]",
        "  G --> J[knowledge/prompts/]",
        "```",
        "",
        "## File Relationship Matrix",
        "| File/Folder | Depends On | Purpose |",
        "|---|---|---|",
        "| `config/sources.yaml` | None | Defines source repositories and branches. |",
        "| `scripts/fetch_sources.py` | `config/sources.yaml` | Downloads/extracts source archives. |",
        "| `scripts/index_files.py` | `data/sources/*` | Creates file and binary manifests. |",
        "| `scripts/extract_entities.py` | `data/sources/*` | Normalizes agents/skills/prompts into catalogs. |",
        "| `scripts/build_canonical.py` | `catalog/*.jsonl` | Builds canonical merged outputs and translation audit. |",
        "| `scripts/build_docs.py` | `catalog/*`, `knowledge/*` | Generates docs and this helper. |",
        "| `scripts/validate_repo.py` | all generated outputs | Enforces quality gates. |",
        "| `knowledge/agents/` | canonical catalogs | Canonical merged agent/subagent definitions. |",
        "| `knowledge/skills/` | canonical catalogs | Canonical skill references. |",
        "| `knowledge/prompts/` | canonical catalogs | Canonical prompt references. |",
        "",
        "## Entry Points",
        f"- Agents: `{len(grouped['agent'])}` canonical files in `knowledge/agents/`",
        f"- Skills: `{len(grouped['skill'])}` canonical files in `knowledge/skills/`",
        f"- Prompts: `{len(grouped['prompt'])}` canonical files in `knowledge/prompts/`",
        "",
        "## Suggested Obsidian Vault Setup",
        "1. Open this repository as an Obsidian vault root.",
        "2. Pin `README.md` and `Obsidian-Helper.md` as navigation notes.",
        "3. Use `knowledge/` for browsing canonical content and `catalog/` for machine-readable source of truth.",
        "4. Use `docs/` when explaining merge strategy or onboarding contributors.",
    ]

    return "\n".join(lines)


def run() -> None:
    source_files = read_csv_rows(CATALOG_DIR / "source_files.csv")
    binary_assets = read_csv_rows(CATALOG_DIR / "binary_assets.csv")
    agents = read_jsonl(CATALOG_DIR / "agents.jsonl")
    skills = read_jsonl(CATALOG_DIR / "skills.jsonl")
    prompts = read_jsonl(CATALOG_DIR / "prompts.jsonl")
    canonical = read_jsonl(CATALOG_DIR / "canonical_entities.jsonl")

    taxonomy_path = CATALOG_DIR / "taxonomy.json"
    taxonomy = json.loads(taxonomy_path.read_text(encoding="utf-8")) if taxonomy_path.exists() else {}

    duplicates_path = CATALOG_DIR / "duplicates_agents.json"
    duplicates = json.loads(duplicates_path.read_text(encoding="utf-8")) if duplicates_path.exists() else {}

    write(DOCS_DIR / "source-map.md", build_source_map(source_files, binary_assets, agents, skills, prompts))
    write(DOCS_DIR / "merge-policy.md", build_merge_policy())
    write(DOCS_DIR / "agent-role-language-system-matrix.md", build_matrix(taxonomy))
    write(DOCS_DIR / "prompt-library.md", build_prompt_library([r for r in canonical if r["entity_type"] == "prompt"]))
    write(DOCS_DIR / "developer-guide.md", build_developer_guide())

    write(REPO_ROOT / "README.md", build_readme(source_files, binary_assets, canonical, duplicates, taxonomy))
    write(REPO_ROOT / "Obsidian-Helper.md", build_obsidian_helper(canonical))

    print("Documentation regenerated")


if __name__ == "__main__":
    run()
