# use_me_codex.md

Use this file when a user gives this repository URL and asks:
"Set up my Codex workspace using this repo."

## Goal

Install this repo's full agents and skills into the user's local Codex setup safely and predictably.

## Default behavior (important)

- Prefer non-destructive install first.
- Do not overwrite existing user files unless user asks.
- Show exactly what was done and where files were installed.
- Run verification commands and report results.

## Standard setup flow

1. Clone or update this repository.
2. Detect install paths:
   - `CODEX_HOME` (default: `~/.codex`)
   - agent target (default: `~/.codex/agents`)
   - skill target (default auto-resolution):
     - use `~/.codex/skills` when `~/.codex/skills` already exists
     - otherwise use `~/.agents/skills` (official Codex skills docs user path)
3. Run safe install script.
4. Verify installed files.
5. Optionally enable global AGENTS guidance (only if user wants it).
6. Optionally export Obsidian bundle (if user asks).

## Commands Codex should run

Use repository root as working directory.

```bash
# 1) safe install (recommended default: catalog + custom overlay)
./scripts/install_codex_helper.sh

# 2) verify
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
if [ -n "${SKILL_TARGET_DIR:-}" ]; then
  RESOLVED_SKILL_TARGET_DIR="$SKILL_TARGET_DIR"
elif [ -d "$CODEX_HOME/skills" ]; then
  RESOLVED_SKILL_TARGET_DIR="$CODEX_HOME/skills"
else
  RESOLVED_SKILL_TARGET_DIR="$HOME/.agents/skills"
fi
ls "$CODEX_HOME/agents"
ls "$RESOLVED_SKILL_TARGET_DIR"

# 3) optional: include/refresh global guidance in ~/.codex/AGENTS.md
./scripts/install_codex_helper.sh --with-global-guidance

# 4) optional: only install custom overlay assets
./scripts/install_codex_helper.sh --custom-only

# 5) optional: only install canonical catalog assets
./scripts/install_codex_helper.sh --catalog-only

# 6) optional: overwrite existing installed assets (only with explicit user confirmation)
./scripts/install_codex_helper.sh --force

# 7) optional: symlink mode for active development (catalog + custom)
./scripts/link_codex_helper.sh
```

## Obsidian no-command path (when asked)

Tell the user they can skip scripts and just copy:

- `for_obsidian/` into their Obsidian vault
- then open `for_obsidian/00_Home.md`

Optional export command:

```bash
./scripts/export_obsidian_bundle.sh "/path/to/ObsidianVault"
```

## What Codex should report back

Always provide:

- commands that were run
- install paths used
- installed/updated files
- skipped files and why (for example, already existed and `--force` not used)
- verification command output summary
- next optional step (for example, global guidance or Obsidian export)

## Troubleshooting quick checks

```bash
./scripts/install_codex_helper.sh --dry-run
./scripts/link_codex_helper.sh --dry-run
echo "${CODEX_HOME:-$HOME/.codex}"
test -d "${CODEX_HOME:-$HOME/.codex}/skills" && echo "codex skills path exists"
test -d "${HOME}/.agents/skills" && echo "agents skills path exists"
```
