#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
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

OBSIDIAN_DIR = REPO_ROOT / "for_obsidian"
OBSIDIAN_CATALOG_DIR = OBSIDIAN_DIR / "catalog"
OBSIDIAN_GRAPH_DIR = OBSIDIAN_DIR / "graph"
OBSIDIAN_GRAPH_AGENT_DIR = OBSIDIAN_GRAPH_DIR / "agents"
OBSIDIAN_GRAPH_SKILL_DIR = OBSIDIAN_GRAPH_DIR / "skills"
OBSIDIAN_GRAPH_PROMPT_DIR = OBSIDIAN_GRAPH_DIR / "prompts"
OBSIDIAN_GRAPH_ROLE_DIR = OBSIDIAN_GRAPH_DIR / "roles"
OBSIDIAN_GRAPH_SYSTEM_DIR = OBSIDIAN_GRAPH_DIR / "systems"
OBSIDIAN_GRAPH_LANGUAGE_DIR = OBSIDIAN_GRAPH_DIR / "languages"
OBSIDIAN_GRAPH_MAP_DIR = OBSIDIAN_GRAPH_DIR / "maps"
OBSIDIAN_GRAPH_PLAYBOOK_DIR = OBSIDIAN_GRAPH_DIR / "playbooks"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def normalize_cell(value: str, limit: int = 180) -> str:
    raw = (value or "").replace("|", " / ").replace(">", " ")
    text = " ".join(raw.split())
    if not any(ch.isalnum() for ch in text):
        text = "No summary available."
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text.replace("|", "\\|")


def record_focus(record: dict) -> str:
    role_part = ", ".join(record.get("roles", [])[:2])
    system_part = ", ".join(record.get("systems", [])[:2])
    language_part = ", ".join(record.get("languages", [])[:2])

    parts = [part for part in [role_part, system_part, language_part] if part]
    return " / ".join(parts[:3]) if parts else "general-purpose support"


def is_subagent_record(record: dict) -> bool:
    refs = record.get("source_refs", [])
    for ref in refs:
        repo = ref.get("source_repo", "").lower()
        path = ref.get("source_path", "").lower()
        if "subagent" in repo:
            return True
        if path.startswith("subagents/"):
            return True
        if "/subagent" in path:
            return True
        if path.startswith("categories/"):
            return True
    return False


def slugify_note(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled"


def wiki_link(path_no_ext: str, label: str | None = None) -> str:
    if label:
        return f"[[{path_no_ext}|{label}]]"
    return f"[[{path_no_ext}]]"


def record_terms(record: dict) -> set[str]:
    terms: set[str] = set()
    for key in ["roles", "systems", "languages", "jobs", "tags"]:
        for value in record.get(key, []):
            value_text = str(value).strip().lower()
            if value_text:
                terms.add(value_text)
    return terms


def top_related_records(target: dict, candidates: list[dict], limit: int = 8) -> list[dict]:
    target_terms = record_terms(target)
    scored: list[tuple[int, str, dict]] = []
    for candidate in candidates:
        if candidate["name"] == target["name"]:
            continue
        overlap = len(target_terms & record_terms(candidate))
        if overlap <= 0:
            continue
        scored.append((overlap, candidate["name"], candidate))

    scored.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in scored[:limit]]


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
    source_count = len(load_sources())

    top_roles = ", ".join(r["name"] for r in taxonomy.get("roles", [])[:8])
    top_languages = ", ".join(r["name"] for r in taxonomy.get("languages", [])[:8])

    return "\n".join(
        [
            "# Codex-Software-Developer",
            "",
            "A copy-ready knowledge kit for Codex.",
            "",
            "It collects AI agents and skills from multiple public libraries, cleans and merges them, and publishes one simple folder you can drop into Obsidian.",
            "",
            "## What We Do (Plain Language)",
            "- Gather many agent and skill collections in one place.",
            "- Remove duplicates and normalize wording so the library is easier to browse.",
            "- Build a structured knowledge base (`knowledge/`) plus a human-friendly Obsidian bundle (`for_obsidian/`).",
            "- Keep the process repeatable with scripts so updates stay consistent.",
            "",
            "## How We Do It (Simple + Detailed)",
            "1. Pull configured source repositories.",
            "2. Index every file and detect text vs binary assets.",
            "3. Extract agents, skills, and prompts into structured records.",
            "4. Merge duplicates into canonical outputs.",
            "5. Generate docs and an Obsidian-ready graph folder.",
            "6. Run validation checks before shipping.",
            "",
            "## Current Snapshot",
            f"- Source repositories configured: **{source_count}**",
            f"- Indexed source files: **{len(source_files)}**",
            f"- Indexed binary assets: **{len(binary_assets)}** (indexed only, not copied)",
            f"- Canonical agents: **{entity_counter.get('agent', 0)}**",
            f"- Canonical skills: **{entity_counter.get('skill', 0)}**",
            f"- Canonical prompts: **{entity_counter.get('prompt', 0)}**",
            f"- Cross-repo duplicate agent names merged: **{duplicates.get('total_duplicate_names', 0)}**",
            "",
            "## Easiest Way To Use This Repo (No Commands)",
            "1. Download the repository ZIP.",
            "2. Copy the `for_obsidian/` folder into your Obsidian vault.",
            "3. Open `for_obsidian/00_Home.md`.",
            "4. For graph exploration, open `for_obsidian/graph/00_Graph_Home.md`.",
            "",
            "## How To Add More Source Repos",
            "Edit `config/sources.yaml` and add another entry:",
            "```yaml",
            "sources:",
            "  - owner: your-org",
            "    repo: your-repo",
            "    branch: main",
            "```",
            "Then run:",
            "```bash",
            "python3 scripts/fetch_sources.py --refresh",
            "python3 scripts/index_files.py",
            "python3 scripts/extract_entities.py",
            "python3 scripts/build_canonical.py",
            "python3 scripts/build_docs.py",
            "python3 scripts/validate_repo.py",
            "```",
            "",
            "## What Each Script Does",
            "| Script | What it does |",
            "|---|---|",
            "| `scripts/fetch_sources.py` | Downloads and extracts all configured source repositories. |",
            "| `scripts/index_files.py` | Indexes source files and tracks binary assets. |",
            "| `scripts/extract_entities.py` | Extracts agents, skills, and prompts into normalized records. |",
            "| `scripts/build_canonical.py` | Merges duplicates and writes canonical outputs into `knowledge/`. |",
            "| `scripts/build_docs.py` | Regenerates `README.md`, docs, and the Obsidian bundle notes. |",
            "| `scripts/validate_repo.py` | Runs integrity checks across indexes, outputs, and links. |",
            "| `scripts/refresh_obsidian_inventory.sh` | Refreshes Obsidian markdown inventory. |",
            "| `scripts/export_obsidian_bundle.sh` | Copies `for_obsidian/` into a target vault folder. |",
            "| `scripts/install_codex_helper.sh` | Installs local agent and skill assets for Codex usage. |",
            "| `scripts/link_codex_helper.sh` | Symlink-based install mode for local development. |",
            "",
            "## How To Use This Repo (Diagram)",
            "```mermaid",
            "flowchart TD",
            '  A["Download ZIP"] --> B["Copy for_obsidian folder into your vault"]',
            '  B --> C["Open for_obsidian/00_Home.md"]',
            '  C --> D["Browse catalogs and graph maps"]',
            '  E["Maintainers: add/edit sources in config/sources.yaml"] --> F["Run pipeline scripts"]',
            '  F --> G["Validate and commit updates"]',
            '  G --> D',
            "```",
            "",
            "## Repository Layout",
            "```text",
            "config/                 # source definitions",
            "scripts/                # reproducible build/index/validate pipeline",
            "catalog/                # machine-readable manifests and normalized contracts",
            "knowledge/agents/       # canonical merged agent TOMLs",
            "knowledge/skills/       # canonical skill markdown",
            "knowledge/prompts/      # canonical prompt markdown",
            "for_obsidian/           # copy-ready vault folder",
            "docs/                   # source map, merge policy, matrix, guide",
            "Obsidian-Helper.md      # vault-first relationship guide",
            "```",
            "",
            "## Taxonomy Highlights",
            f"- Top roles: {top_roles or 'n/a'}",
            f"- Top languages: {top_languages or 'n/a'}",
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
        "  A --> K[for_obsidian/]",
        "  K --> L[for_obsidian/11_Capability_Catalog.md]",
        "  K --> M[for_obsidian/catalog/*]",
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
        "| `for_obsidian/catalog/` | canonical catalogs | User-facing capability map for Obsidian. |",
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


def build_obsidian_catalog_home(canonical: list[dict], taxonomy: dict) -> str:
    grouped = defaultdict(list)
    for record in canonical:
        grouped[record["entity_type"]].append(record)

    subagent_count = sum(1 for record in grouped["agent"] if is_subagent_record(record))
    top_roles = taxonomy.get("roles", [])[:20]
    top_systems = taxonomy.get("systems", [])[:20]

    lines = [
        "---",
        "tags: [codex, obsidian, catalog, capabilities]",
        "---",
        "",
        "# Capability Catalog",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "This note is your single jump point for all installed capability profiles.",
        "",
        "## Catalog views",
        "",
        "| View | What it includes | Link |",
        "|---|---|---|",
        f"| Full agents | All canonical agent profiles ({len(grouped['agent'])}) | [[catalog/01_Agents_Full]] |",
        f"| Full subagents | Subagent-style profiles ({subagent_count}) | [[catalog/02_Subagents_Full]] |",
        f"| Full skills | All canonical skills ({len(grouped['skill'])}) | [[catalog/03_Skills_Full]] |",
        f"| Full prompts | Canonical prompts ({len(grouped['prompt'])}) | [[catalog/04_Prompts_Full]] |",
        "| Capability matrix | Top role/system/language coverage and starter workflows | [[catalog/05_What_You_Can_Do]] |",
        "| Graph-first explorer | Fully connected nodes for roles, systems, languages, agents, and skills | [[graph/00_Graph_Home]] |",
        "",
        "## Top capability roles",
        "",
        "| Role | Coverage |",
        "|---|---:|",
    ]

    for row in top_roles:
        lines.append(f"| `{normalize_cell(row['name'], 80)}` | {row['count']} |")

    lines.extend(["", "## Top systems", "", "| System | Coverage |", "|---|---:|"])
    for row in top_systems:
        lines.append(f"| `{normalize_cell(row['name'], 80)}` | {row['count']} |")

    lines.extend(
        [
            "",
            "## Linked views",
            "",
            "- [[00_Home]]",
            "- [[02_Agents]]",
            "- [[03_Skills]]",
            "- [[06_Decision_Guide]]",
            "- [[graph/00_Graph_Home]]",
        ]
    )

    return "\n".join(lines)


def build_obsidian_agents_catalog(agents: list[dict]) -> str:
    sorted_agents = sorted(agents, key=lambda r: r["name"])
    lines = [
        "---",
        "tags: [codex, agents, catalog, full-list]",
        "---",
        "",
        "# All Agents",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        f"Total canonical agents: **{len(sorted_agents)}**",
        "",
        "| Agent | What it does | Best for |",
        "|---|---|---|",
    ]

    for record in sorted_agents:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{normalize_cell(record['name'], 120)}`",
                    normalize_cell(record.get("summary", ""), 220),
                    normalize_cell(record_focus(record), 200),
                ]
            )
            + " |"
        )

    lines.extend(["", "Back to [[11_Capability_Catalog]]."])
    return "\n".join(lines)


def build_obsidian_subagents_catalog(agents: list[dict]) -> str:
    subagents = sorted((record for record in agents if is_subagent_record(record)), key=lambda r: r["name"])
    lines = [
        "---",
        "tags: [codex, subagents, catalog, full-list]",
        "---",
        "",
        "# All Subagents",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        f"Total subagent-style profiles: **{len(subagents)}**",
        "",
        "| Subagent | What it does | Best for |",
        "|---|---|---|",
    ]

    for record in subagents:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{normalize_cell(record['name'], 120)}`",
                    normalize_cell(record.get("summary", ""), 220),
                    normalize_cell(record_focus(record), 200),
                ]
            )
            + " |"
        )

    lines.extend(["", "Back to [[11_Capability_Catalog]]."])
    return "\n".join(lines)


def build_obsidian_skills_catalog(skills: list[dict]) -> str:
    sorted_skills = sorted(skills, key=lambda r: r["name"])
    lines = [
        "---",
        "tags: [codex, skills, catalog, full-list]",
        "---",
        "",
        "# All Skills",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        f"Total canonical skills: **{len(sorted_skills)}**",
        "",
        "| Skill | What it does | Best for |",
        "|---|---|---|",
    ]

    for record in sorted_skills:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{normalize_cell(record['name'], 120)}`",
                    normalize_cell(record.get("summary", ""), 220),
                    normalize_cell(record_focus(record), 200),
                ]
            )
            + " |"
        )

    lines.extend(["", "Back to [[11_Capability_Catalog]]."])
    return "\n".join(lines)


def build_obsidian_prompts_catalog(prompts: list[dict]) -> str:
    sorted_prompts = sorted(prompts, key=lambda r: r["name"])
    lines = [
        "---",
        "tags: [codex, prompts, catalog, full-list]",
        "---",
        "",
        "# All Prompts",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        f"Total canonical prompts: **{len(sorted_prompts)}**",
        "",
        "| Prompt | Purpose | Focus areas |",
        "|---|---|---|",
    ]

    for record in sorted_prompts:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{normalize_cell(record['name'], 120)}`",
                    normalize_cell(record.get("summary", ""), 220),
                    normalize_cell(record_focus(record), 200),
                ]
            )
            + " |"
        )

    lines.extend(["", "Back to [[11_Capability_Catalog]]."])
    return "\n".join(lines)


def pick_first_existing(records_by_name: set[str], candidates: list[str]) -> str:
    for candidate in candidates:
        if candidate in records_by_name:
            return f"`{candidate}`"
    return "n/a"


def build_obsidian_capability_matrix(agents: list[dict], skills: list[dict], taxonomy: dict) -> str:
    top_roles = taxonomy.get("roles", [])[:40]
    top_languages = taxonomy.get("languages", [])[:25]
    top_systems = taxonomy.get("systems", [])[:25]

    agent_names = {record["name"] for record in agents}
    skill_names = {record["name"] for record in skills}

    workflow_rows = [
        (
            "Codebase discovery and mapping",
            ["code-mapper", "code-archaeologist", "architect-review"],
            ["codebase-orientation", "create-plan", "read-github"],
        ),
        (
            "Implementation delivery",
            ["backend-developer", "frontend-developer", "fullstack-developer"],
            ["ticket-breakdown", "unit-test-starter", "simple-refactor"],
        ),
        (
            "Risk and review before merge",
            ["code-reviewer", "security-auditor", "tester"],
            ["pr-reviewer", "security-quick-scan", "release-notes-drafter"],
        ),
        (
            "Performance and scale tuning",
            ["performance-engineer", "performance-optimizer", "database-optimizer"],
            ["performance-budgeting", "performance-trace-guide", "scalability-assessment"],
        ),
        (
            "Infra and deployment setup",
            ["devops-engineer", "deployment-engineer", "cloud-architect"],
            ["zero-downtime-migration", "config-hardening", "platform-migration-plan"],
        ),
        (
            "Documentation and communication",
            ["documentation-engineer", "technical-writer", "api-documenter"],
            ["readme-polish", "function-docstrings", "internal-comms"],
        ),
    ]

    lines = [
        "---",
        "tags: [codex, capabilities, matrix, workflows]",
        "---",
        "",
        "# What You Can Do",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## Starter workflows",
        "",
        "| Outcome | Suggested agent | Suggested skill |",
        "|---|---|---|",
    ]

    for outcome, agent_options, skill_options in workflow_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    normalize_cell(outcome, 120),
                    pick_first_existing(agent_names, agent_options),
                    pick_first_existing(skill_names, skill_options),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Role coverage", "", "| Role | Count |", "|---|---:|"])
    for row in top_roles:
        lines.append(f"| `{normalize_cell(row['name'], 80)}` | {row['count']} |")

    lines.extend(["", "## System coverage", "", "| System | Count |", "|---|---:|"])
    for row in top_systems:
        lines.append(f"| `{normalize_cell(row['name'], 80)}` | {row['count']} |")

    lines.extend(["", "## Language coverage", "", "| Language | Count |", "|---|---:|"])
    for row in top_languages:
        lines.append(f"| `{normalize_cell(row['name'], 80)}` | {row['count']} |")

    lines.extend(["", "Back to [[11_Capability_Catalog]]."])
    return "\n".join(lines)


def select_records_by_keywords(records: list[dict], keywords: list[str], limit: int = 12) -> list[dict]:
    scored: list[tuple[int, str, dict]] = []
    keywords_lower = [k.lower() for k in keywords]
    for record in records:
        haystack = " ".join(
            [
                record.get("name", ""),
                record.get("summary", ""),
                " ".join(record.get("roles", [])),
                " ".join(record.get("systems", [])),
                " ".join(record.get("languages", [])),
                " ".join(record.get("tags", [])),
            ]
        ).lower()
        score = sum(1 for keyword in keywords_lower if keyword in haystack)
        if score <= 0:
            continue
        scored.append((score, record["name"], record))
    scored.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in scored[:limit]]


def bullet_links(links: list[str]) -> list[str]:
    if not links:
        return ["- none"]
    return [f"- {link}" for link in links]


def build_obsidian_graph_home(
    agents: list[dict],
    skills: list[dict],
    prompts: list[dict],
    playbook_names: list[tuple[str, str]],
) -> str:
    lines = [
        "---",
        "tags: [codex, graph, home]",
        "---",
        "",
        "# Graph Home",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "This graph-first section is optimized for Obsidian exploration.",
        "",
        "## Start points",
        "",
        "| View | Link |",
        "|---|---|",
        "| Capability universe map | [[graph/maps/capability-universe]] |",
        "| Roles map | [[graph/maps/by-role]] |",
        "| Systems map | [[graph/maps/by-system]] |",
        "| Languages map | [[graph/maps/by-language]] |",
        f"| Agent nodes | [[graph/agents/_index]] ({len(agents)} notes) |",
        f"| Skill nodes | [[graph/skills/_index]] ({len(skills)} notes) |",
        f"| Prompt nodes | [[graph/prompts/_index]] ({len(prompts)} notes) |",
        "",
        "## High-value playbooks",
    ]

    for slug, title in playbook_names:
        lines.append(f"- {wiki_link(f'graph/playbooks/{slug}', title)}")

    lines.extend(
        [
            "",
            "## Linked views",
            "- [[00_Home]]",
            "- [[11_Capability_Catalog]]",
            "",
            "## Universe graph",
            "```mermaid",
            "graph LR",
            '  A["Graph Home"] --> B["Capability Universe"]',
            '  A --> C["Roles"]',
            '  A --> D["Systems"]',
            '  A --> E["Languages"]',
            '  A --> F["Agent Nodes"]',
            '  A --> G["Skill Nodes"]',
            '  A --> H["Prompt Nodes"]',
            '  B --> I["Playbooks"]',
            "```",
        ]
    )
    return "\n".join(lines)


def build_obsidian_graph_dimension_map(
    title: str,
    tag: str,
    folder: str,
    rows: list[tuple[str, int, int]],
) -> str:
    lines = [
        "---",
        f"tags: [codex, graph, {tag}]",
        "---",
        "",
        f"# {title}",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "| Node | Agent links | Skill links |",
        "|---|---:|---:|",
    ]
    for name, agent_count, skill_count in rows:
        slug = slugify_note(name)
        lines.append(
            f"| {wiki_link(f'graph/{folder}/{slug}', name)} | {agent_count} | {skill_count} |"
        )

    lines.extend(
        [
            "",
            "## Linked views",
            "- [[graph/00_Graph_Home]]",
            "- [[11_Capability_Catalog]]",
        ]
    )
    return "\n".join(lines)


def build_obsidian_graph_dimension_node(
    title_prefix: str,
    name: str,
    agent_links: list[str],
    skill_links: list[str],
) -> str:
    lines = [
        "---",
        "tags: [codex, graph, node]",
        "---",
        "",
        f"# {title_prefix}: {name}",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        f"Connected agent nodes: **{len(agent_links)}**",
        f"Connected skill nodes: **{len(skill_links)}**",
        "",
        "## Agent nodes",
        *bullet_links(agent_links),
        "",
        "## Skill nodes",
        *bullet_links(skill_links),
        "",
        "## Linked views",
        "- [[graph/00_Graph_Home]]",
        "- [[11_Capability_Catalog]]",
    ]
    return "\n".join(lines)


def build_obsidian_graph_agent_node(
    agent: dict,
    agent_slug: dict[str, str],
    skill_slug: dict[str, str],
    prompt_slug: dict[str, str],
    role_slug: dict[str, str],
    system_slug: dict[str, str],
    language_slug: dict[str, str],
    all_skills: list[dict],
    all_prompts: list[dict],
) -> str:
    roles = [wiki_link(f"graph/roles/{role_slug[r]}", r) for r in agent.get("roles", []) if r in role_slug]
    systems = [wiki_link(f"graph/systems/{system_slug[s]}", s) for s in agent.get("systems", []) if s in system_slug]
    languages = [
        wiki_link(f"graph/languages/{language_slug[l]}", l)
        for l in agent.get("languages", [])
        if l in language_slug
    ]

    related_skills = top_related_records(agent, all_skills, limit=12)
    skill_links = [wiki_link(f"graph/skills/{skill_slug[s['name']]}", s["name"]) for s in related_skills if s["name"] in skill_slug]

    related_prompts = top_related_records(agent, all_prompts, limit=8)
    prompt_links = [wiki_link(f"graph/prompts/{prompt_slug[p['name']]}", p["name"]) for p in related_prompts if p["name"] in prompt_slug]

    lines = [
        "---",
        "tags: [codex, graph, agent]",
        "---",
        "",
        f"# Agent Node: {agent['name']}",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## What this node does",
        normalize_cell(agent.get("summary", ""), 600),
        "",
        "## Connected roles",
        *bullet_links(roles),
        "",
        "## Connected systems",
        *bullet_links(systems),
        "",
        "## Connected languages",
        *bullet_links(languages),
        "",
        "## Related skill nodes",
        *bullet_links(skill_links),
        "",
        "## Related prompt nodes",
        *bullet_links(prompt_links),
        "",
        "## Linked views",
        "- [[graph/00_Graph_Home]]",
        "- [[11_Capability_Catalog]]",
    ]
    return "\n".join(lines)


def build_obsidian_graph_skill_node(
    skill: dict,
    agent_slug: dict[str, str],
    prompt_slug: dict[str, str],
    role_slug: dict[str, str],
    system_slug: dict[str, str],
    language_slug: dict[str, str],
    all_agents: list[dict],
    all_prompts: list[dict],
) -> str:
    roles = [wiki_link(f"graph/roles/{role_slug[r]}", r) for r in skill.get("roles", []) if r in role_slug]
    systems = [wiki_link(f"graph/systems/{system_slug[s]}", s) for s in skill.get("systems", []) if s in system_slug]
    languages = [
        wiki_link(f"graph/languages/{language_slug[l]}", l)
        for l in skill.get("languages", [])
        if l in language_slug
    ]

    related_agents = top_related_records(skill, all_agents, limit=12)
    agent_links = [wiki_link(f"graph/agents/{agent_slug[a['name']]}", a["name"]) for a in related_agents if a["name"] in agent_slug]

    related_prompts = top_related_records(skill, all_prompts, limit=8)
    prompt_links = [wiki_link(f"graph/prompts/{prompt_slug[p['name']]}", p["name"]) for p in related_prompts if p["name"] in prompt_slug]

    lines = [
        "---",
        "tags: [codex, graph, skill]",
        "---",
        "",
        f"# Skill Node: {skill['name']}",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## What this node does",
        normalize_cell(skill.get("summary", ""), 600),
        "",
        "## Connected roles",
        *bullet_links(roles),
        "",
        "## Connected systems",
        *bullet_links(systems),
        "",
        "## Connected languages",
        *bullet_links(languages),
        "",
        "## Related agent nodes",
        *bullet_links(agent_links),
        "",
        "## Related prompt nodes",
        *bullet_links(prompt_links),
        "",
        "## Linked views",
        "- [[graph/00_Graph_Home]]",
        "- [[11_Capability_Catalog]]",
    ]
    return "\n".join(lines)


def build_obsidian_graph_prompt_node(
    prompt: dict,
    agent_slug: dict[str, str],
    skill_slug: dict[str, str],
    role_slug: dict[str, str],
    system_slug: dict[str, str],
    language_slug: dict[str, str],
    all_agents: list[dict],
    all_skills: list[dict],
) -> str:
    roles = [wiki_link(f"graph/roles/{role_slug[r]}", r) for r in prompt.get("roles", []) if r in role_slug]
    systems = [wiki_link(f"graph/systems/{system_slug[s]}", s) for s in prompt.get("systems", []) if s in system_slug]
    languages = [
        wiki_link(f"graph/languages/{language_slug[l]}", l)
        for l in prompt.get("languages", [])
        if l in language_slug
    ]

    related_agents = top_related_records(prompt, all_agents, limit=10)
    related_skills = top_related_records(prompt, all_skills, limit=10)
    agent_links = [wiki_link(f"graph/agents/{agent_slug[a['name']]}", a["name"]) for a in related_agents if a["name"] in agent_slug]
    skill_links = [wiki_link(f"graph/skills/{skill_slug[s['name']]}", s["name"]) for s in related_skills if s["name"] in skill_slug]

    lines = [
        "---",
        "tags: [codex, graph, prompt]",
        "---",
        "",
        f"# Prompt Node: {prompt['name']}",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "## What this node does",
        normalize_cell(prompt.get("summary", ""), 600),
        "",
        "## Connected roles",
        *bullet_links(roles),
        "",
        "## Connected systems",
        *bullet_links(systems),
        "",
        "## Connected languages",
        *bullet_links(languages),
        "",
        "## Related agent nodes",
        *bullet_links(agent_links),
        "",
        "## Related skill nodes",
        *bullet_links(skill_links),
        "",
        "## Linked views",
        "- [[graph/00_Graph_Home]]",
        "- [[11_Capability_Catalog]]",
    ]
    return "\n".join(lines)


def build_obsidian_playbook_node(
    title: str,
    description: str,
    agents: list[dict],
    skills: list[dict],
    prompts: list[dict],
    agent_slug: dict[str, str],
    skill_slug: dict[str, str],
    prompt_slug: dict[str, str],
) -> str:
    agent_links = [wiki_link(f"graph/agents/{agent_slug[a['name']]}", a["name"]) for a in agents if a["name"] in agent_slug]
    skill_links = [wiki_link(f"graph/skills/{skill_slug[s['name']]}", s["name"]) for s in skills if s["name"] in skill_slug]
    prompt_links = [wiki_link(f"graph/prompts/{prompt_slug[p['name']]}", p["name"]) for p in prompts if p["name"] in prompt_slug]

    lines = [
        "---",
        "tags: [codex, graph, playbook]",
        "---",
        "",
        f"# Playbook: {title}",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        description,
        "",
        "## Suggested agent nodes",
        *bullet_links(agent_links),
        "",
        "## Suggested skill nodes",
        *bullet_links(skill_links),
        "",
        "## Suggested prompt nodes",
        *bullet_links(prompt_links),
        "",
        "## Linked views",
        "- [[graph/00_Graph_Home]]",
        "- [[11_Capability_Catalog]]",
    ]
    return "\n".join(lines)


def build_obsidian_capability_universe_map(playbook_names: list[tuple[str, str]]) -> str:
    lines = [
        "---",
        "tags: [codex, graph, map, mermaid]",
        "---",
        "",
        "# Capability Universe",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
        "```mermaid",
        "graph TD",
        '  A["Codex Capability Universe"] --> B["Role Nodes"]',
        '  A --> C["System Nodes"]',
        '  A --> D["Language Nodes"]',
        '  A --> E["Agent Nodes"]',
        '  A --> F["Skill Nodes"]',
        '  A --> G["Prompt Nodes"]',
        '  A --> H["Playbooks"]',
    ]

    for slug, title in playbook_names:
        lines.append(f'  H --> P_{slug.replace("-", "_")}["{title}"]')

    lines.extend(
        [
            "```",
            "",
            "## Linked views",
            "- [[graph/00_Graph_Home]]",
            "- [[graph/maps/by-role]]",
            "- [[graph/maps/by-system]]",
            "- [[graph/maps/by-language]]",
        ]
    )
    return "\n".join(lines)


def build_obsidian_graph_indexes(
    agents: list[dict],
    skills: list[dict],
    prompts: list[dict],
    agent_slug: dict[str, str],
    skill_slug: dict[str, str],
    prompt_slug: dict[str, str],
) -> dict[Path, str]:
    agent_index_lines = [
        "---",
        "tags: [codex, graph, agents, index]",
        "---",
        "",
        "# Agent Node Index",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
    ]
    for agent in sorted(agents, key=lambda r: r["name"]):
        link = wiki_link(f"graph/agents/{agent_slug[agent['name']]}", agent["name"])
        agent_index_lines.append(f"- {link}")

    skill_index_lines = [
        "---",
        "tags: [codex, graph, skills, index]",
        "---",
        "",
        "# Skill Node Index",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
    ]
    for skill in sorted(skills, key=lambda r: r["name"]):
        link = wiki_link(f"graph/skills/{skill_slug[skill['name']]}", skill["name"])
        skill_index_lines.append(f"- {link}")

    prompt_index_lines = [
        "---",
        "tags: [codex, graph, prompts, index]",
        "---",
        "",
        "# Prompt Node Index",
        "",
        f"Generated at: `{utc_now_iso()}`",
        "",
    ]
    for prompt in sorted(prompts, key=lambda r: r["name"]):
        link = wiki_link(f"graph/prompts/{prompt_slug[prompt['name']]}", prompt["name"])
        prompt_index_lines.append(f"- {link}")

    return {
        OBSIDIAN_GRAPH_AGENT_DIR / "_index.md": "\n".join(agent_index_lines),
        OBSIDIAN_GRAPH_SKILL_DIR / "_index.md": "\n".join(skill_index_lines),
        OBSIDIAN_GRAPH_PROMPT_DIR / "_index.md": "\n".join(prompt_index_lines),
    }


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

    canonical_agents = [r for r in canonical if r["entity_type"] == "agent"]
    canonical_skills = [r for r in canonical if r["entity_type"] == "skill"]
    canonical_prompts = [r for r in canonical if r["entity_type"] == "prompt"]

    write(OBSIDIAN_DIR / "11_Capability_Catalog.md", build_obsidian_catalog_home(canonical, taxonomy))
    write(OBSIDIAN_CATALOG_DIR / "01_Agents_Full.md", build_obsidian_agents_catalog(canonical_agents))
    write(OBSIDIAN_CATALOG_DIR / "02_Subagents_Full.md", build_obsidian_subagents_catalog(canonical_agents))
    write(OBSIDIAN_CATALOG_DIR / "03_Skills_Full.md", build_obsidian_skills_catalog(canonical_skills))
    write(OBSIDIAN_CATALOG_DIR / "04_Prompts_Full.md", build_obsidian_prompts_catalog(canonical_prompts))
    write(
        OBSIDIAN_CATALOG_DIR / "05_What_You_Can_Do.md",
        build_obsidian_capability_matrix(canonical_agents, canonical_skills, taxonomy),
    )

    if OBSIDIAN_GRAPH_DIR.exists():
        shutil.rmtree(OBSIDIAN_GRAPH_DIR)

    all_records = canonical_agents + canonical_skills + canonical_prompts

    agent_slug = {record["name"]: slugify_note(record["name"]) for record in canonical_agents}
    skill_slug = {record["name"]: slugify_note(record["name"]) for record in canonical_skills}
    prompt_slug = {record["name"]: slugify_note(record["name"]) for record in canonical_prompts}

    roles = sorted({value for record in all_records for value in record.get("roles", [])})
    systems = sorted({value for record in all_records for value in record.get("systems", [])})
    languages = sorted({value for record in all_records for value in record.get("languages", [])})

    role_slug = {role: slugify_note(role) for role in roles}
    system_slug = {system: slugify_note(system) for system in systems}
    language_slug = {language: slugify_note(language) for language in languages}

    role_to_agents: dict[str, list[dict]] = defaultdict(list)
    role_to_skills: dict[str, list[dict]] = defaultdict(list)
    system_to_agents: dict[str, list[dict]] = defaultdict(list)
    system_to_skills: dict[str, list[dict]] = defaultdict(list)
    language_to_agents: dict[str, list[dict]] = defaultdict(list)
    language_to_skills: dict[str, list[dict]] = defaultdict(list)

    for record in canonical_agents:
        for role in record.get("roles", []):
            role_to_agents[role].append(record)
        for system in record.get("systems", []):
            system_to_agents[system].append(record)
        for language in record.get("languages", []):
            language_to_agents[language].append(record)

    for record in canonical_skills:
        for role in record.get("roles", []):
            role_to_skills[role].append(record)
        for system in record.get("systems", []):
            system_to_skills[system].append(record)
        for language in record.get("languages", []):
            language_to_skills[language].append(record)

    playbook_specs = [
        (
            "frontend-developer",
            "Frontend Developer",
            "Use this path when building UI-heavy product work across components, interaction patterns, and browser behavior.",
            ["frontend", "react", "nextjs", "vue", "angular", "css", "ui", "web", "accessibility"],
        ),
        (
            "backend-developer",
            "Backend Developer",
            "Use this path for service logic, APIs, data models, and backend architecture decisions.",
            ["backend", "api", "database", "service", "microservice", "graphql", "django", "fastapi", "laravel", "spring"],
        ),
        (
            "devops-and-cloud",
            "DevOps And Cloud",
            "Use this path for CI/CD, infrastructure automation, deployment safety, and cloud operations.",
            ["devops", "deployment", "kubernetes", "docker", "terraform", "cloud", "sre", "observability", "incident"],
        ),
        (
            "data-and-ml",
            "Data And ML",
            "Use this path for data engineering, analytics, model integration, and ML operations.",
            ["data", "ml", "machine", "analytics", "pipeline", "model", "sql", "vector", "rag"],
        ),
        (
            "security-and-review",
            "Security And Review",
            "Use this path for risk scans, compliance checks, threat modeling, and final review workflows.",
            ["security", "review", "auditor", "threat", "compliance", "owasp", "penetration"],
        ),
        (
            "mobile-ios-android",
            "Mobile iOS Android",
            "Use this path for app development, debugging, and release work on mobile platforms.",
            ["mobile", "ios", "android", "swift", "swiftui", "react-native", "flutter"],
        ),
    ]
    playbook_names = [(slug, title) for slug, title, _, _ in playbook_specs]

    write(
        OBSIDIAN_GRAPH_DIR / "00_Graph_Home.md",
        build_obsidian_graph_home(canonical_agents, canonical_skills, canonical_prompts, playbook_names),
    )
    write(
        OBSIDIAN_GRAPH_MAP_DIR / "capability-universe.md",
        build_obsidian_capability_universe_map(playbook_names),
    )

    role_rows = [
        (role, len(role_to_agents.get(role, [])), len(role_to_skills.get(role, [])))
        for role in roles
    ]
    system_rows = [
        (system, len(system_to_agents.get(system, [])), len(system_to_skills.get(system, [])))
        for system in systems
    ]
    language_rows = [
        (language, len(language_to_agents.get(language, [])), len(language_to_skills.get(language, [])))
        for language in languages
    ]

    write(
        OBSIDIAN_GRAPH_MAP_DIR / "by-role.md",
        build_obsidian_graph_dimension_map("Role Map", "roles", "roles", role_rows),
    )
    write(
        OBSIDIAN_GRAPH_MAP_DIR / "by-system.md",
        build_obsidian_graph_dimension_map("System Map", "systems", "systems", system_rows),
    )
    write(
        OBSIDIAN_GRAPH_MAP_DIR / "by-language.md",
        build_obsidian_graph_dimension_map("Language Map", "languages", "languages", language_rows),
    )

    for role in roles:
        agent_links = [
            wiki_link(f"graph/agents/{agent_slug[record['name']]}", record["name"])
            for record in sorted(role_to_agents.get(role, []), key=lambda r: r["name"])
            if record["name"] in agent_slug
        ]
        skill_links = [
            wiki_link(f"graph/skills/{skill_slug[record['name']]}", record["name"])
            for record in sorted(role_to_skills.get(role, []), key=lambda r: r["name"])
            if record["name"] in skill_slug
        ]
        write(
            OBSIDIAN_GRAPH_ROLE_DIR / f"{role_slug[role]}.md",
            build_obsidian_graph_dimension_node("Role Node", role, agent_links, skill_links),
        )

    for system in systems:
        agent_links = [
            wiki_link(f"graph/agents/{agent_slug[record['name']]}", record["name"])
            for record in sorted(system_to_agents.get(system, []), key=lambda r: r["name"])
            if record["name"] in agent_slug
        ]
        skill_links = [
            wiki_link(f"graph/skills/{skill_slug[record['name']]}", record["name"])
            for record in sorted(system_to_skills.get(system, []), key=lambda r: r["name"])
            if record["name"] in skill_slug
        ]
        write(
            OBSIDIAN_GRAPH_SYSTEM_DIR / f"{system_slug[system]}.md",
            build_obsidian_graph_dimension_node("System Node", system, agent_links, skill_links),
        )

    for language in languages:
        agent_links = [
            wiki_link(f"graph/agents/{agent_slug[record['name']]}", record["name"])
            for record in sorted(language_to_agents.get(language, []), key=lambda r: r["name"])
            if record["name"] in agent_slug
        ]
        skill_links = [
            wiki_link(f"graph/skills/{skill_slug[record['name']]}", record["name"])
            for record in sorted(language_to_skills.get(language, []), key=lambda r: r["name"])
            if record["name"] in skill_slug
        ]
        write(
            OBSIDIAN_GRAPH_LANGUAGE_DIR / f"{language_slug[language]}.md",
            build_obsidian_graph_dimension_node("Language Node", language, agent_links, skill_links),
        )

    for slug, title, description, keywords in playbook_specs:
        selected_agents = select_records_by_keywords(canonical_agents, keywords, limit=14)
        selected_skills = select_records_by_keywords(canonical_skills, keywords, limit=14)
        selected_prompts = select_records_by_keywords(canonical_prompts, keywords, limit=8)
        write(
            OBSIDIAN_GRAPH_PLAYBOOK_DIR / f"{slug}.md",
            build_obsidian_playbook_node(
                title,
                description,
                selected_agents,
                selected_skills,
                selected_prompts,
                agent_slug,
                skill_slug,
                prompt_slug,
            ),
        )

    for record in sorted(canonical_agents, key=lambda r: r["name"]):
        write(
            OBSIDIAN_GRAPH_AGENT_DIR / f"{agent_slug[record['name']]}.md",
            build_obsidian_graph_agent_node(
                record,
                agent_slug,
                skill_slug,
                prompt_slug,
                role_slug,
                system_slug,
                language_slug,
                canonical_skills,
                canonical_prompts,
            ),
        )

    for record in sorted(canonical_skills, key=lambda r: r["name"]):
        write(
            OBSIDIAN_GRAPH_SKILL_DIR / f"{skill_slug[record['name']]}.md",
            build_obsidian_graph_skill_node(
                record,
                agent_slug,
                prompt_slug,
                role_slug,
                system_slug,
                language_slug,
                canonical_agents,
                canonical_prompts,
            ),
        )

    for record in sorted(canonical_prompts, key=lambda r: r["name"]):
        write(
            OBSIDIAN_GRAPH_PROMPT_DIR / f"{prompt_slug[record['name']]}.md",
            build_obsidian_graph_prompt_node(
                record,
                agent_slug,
                skill_slug,
                role_slug,
                system_slug,
                language_slug,
                canonical_agents,
                canonical_skills,
            ),
        )

    for path, content in build_obsidian_graph_indexes(
        canonical_agents,
        canonical_skills,
        canonical_prompts,
        agent_slug,
        skill_slug,
        prompt_slug,
    ).items():
        write(path, content)

    print("Documentation regenerated")


if __name__ == "__main__":
    run()
