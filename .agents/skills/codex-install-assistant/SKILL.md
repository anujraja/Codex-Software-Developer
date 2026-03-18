---
name: codex-install-assistant
description: Use for local Codex setup, migration, and syncing this repo's skills/agents into user installs.
---

# Codex Install Assistant

## Use this skill when
- someone asks to install or update Codex assets locally
- someone needs a safe migration from one Codex home layout to another
- someone wants script + manual setup instructions

## Workflow

1. Detect target install paths (`$CODEX_HOME`, `~/.codex`, `~/.agents/skills`).
2. Prefer non-destructive copy behavior by default.
3. Back up existing target files before overwrite operations.
4. Provide both a one-command script path and a human-readable manual path.
5. Include a post-install verification checklist.

## Output contract

Always return:
- exact commands run
- files copied/updated
- any skipped paths and why
- verification commands
