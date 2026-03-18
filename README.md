# Codex-Software-Developer

Canonical, English-first, reproducible knowledge base for Codex agents, subagents, skills, roles, jobs, systems, prompts, and workflows.

## What This Repo Does
- Aggregates multiple public agent/skill repositories into one canonical index.
- Deduplicates agent names and generates one merged canonical definition per name.
- Preserves detailed provenance for every canonical output file.
- Builds Obsidian-friendly docs and relationship maps.

## Source Repositories
- `am-will/codex-skills` (`main`)
- `proflead/codex-skills-library` (`master`)
- `VoltAgent/awesome-codex-subagents` (`main`)
- `Dimillian/Skills` (`main`)
- `ComposioHQ/awesome-codex-skills` (`master`)
- `msitarzewski/agency-agents` (`main`)

## Current Snapshot
- Indexed source files: **1280**
- Indexed binary assets: **57** (indexed only, not copied)
- Canonical agents: **473**
- Canonical skills: **130**
- Canonical prompts: **20**
- Cross-repo duplicate agent names merged: **51**

## Taxonomy Highlights
- Top roles: expert, architect, engineer, developer, specialist, manager, admin, orchestrator
- Top languages: sql, c, javascript, python, typescript, swift, react, java

## Repository Layout
```text
config/                 # source definitions
scripts/                # reproducible build/index/validate pipeline
catalog/                # machine-readable manifests and normalized contracts
knowledge/agents/       # canonical merged agent TOMLs
knowledge/skills/       # canonical skill markdown
knowledge/prompts/      # canonical prompt markdown
docs/                   # source map, merge policy, matrix, guide
Obsidian-Helper.md      # vault-first relationship guide
```

## Quickstart
```bash
python3 scripts/fetch_sources.py
python3 scripts/index_files.py
python3 scripts/extract_entities.py
python3 scripts/build_canonical.py
python3 scripts/build_docs.py
python3 scripts/validate_repo.py
```

## Key Contracts
Every canonical entity follows this schema:
- `id`, `name`, `entity_type`, `summary`, `instructions`, `tags`,
- `languages`, `systems`, `jobs`, `roles`, `steps`, `source_refs[]`, `translation_status`

## Detailed Docs
- [Source Map](docs/source-map.md)
- [Merge Policy](docs/merge-policy.md)
- [Agent Role Language System Matrix](docs/agent-role-language-system-matrix.md)
- [Prompt Library](docs/prompt-library.md)
- [Developer Guide](docs/developer-guide.md)
- [Obsidian Helper](Obsidian-Helper.md)
