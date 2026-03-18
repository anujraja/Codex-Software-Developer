# Codex Helper Repository Instructions

This repository is the source of truth for a portable Codex setup kit.

## Primary objective

Keep this repo as a one-stop package that:
- installs custom agents and skills into a local Codex environment
- provides operational guidance for human users
- exports an Obsidian-ready knowledge graph folder

## Routing guide (for Codex)

Use the smallest effective surface for each task.

| Task type | Preferred skill/agent | Why |
|---|---|---|
| Local setup, installation, migration | `$codex-install-assistant` | It enforces safe local install and sync workflows. |
| Obsidian graph notes, knowledge linking | `$obsidian-vault-map` | It standardizes linked-note structure and readable graph topology. |
| Release readiness, repo quality checks | `$release-audit` | It forces test/risk/checklist coverage before shipping. |
| Codebase discovery before edits | built-in `explorer` | Fast read-only exploration with low overhead. |
| Isolated implementation chunks | built-in `worker` | Clear ownership and bounded write scopes. |
| Documentation verification | custom `docs_researcher` agent | Keeps docs checks focused and source-cited. |
| Risk-focused review | custom `reviewer` agent | Prioritizes correctness, regression, and tests. |

## Working rules

- Keep installation scripts non-destructive by default.
- Prefer additive updates to user-level Codex config and AGENTS files.
- Ensure any new markdown docs are represented in `for_obsidian/90_Markdown_Inventory.md`.
- Keep OpenAI documentation references current when changing setup guidance.

## Definition of done

A change is complete only when:
1. docs are updated
2. `for_obsidian` links remain valid and useful
3. install scripts are still runnable and documented
