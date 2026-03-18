# Get All Agents And Skills Locally

This guide gives both script-based and manual installation methods.

## Script method (recommended)

From this repo root:

```bash
./scripts/install_codex_helper.sh
```

Skill target default behavior:
- if `~/.codex/skills` already exists, scripts install/link skills there
- otherwise scripts use `~/.agents/skills` (official Codex docs user-level skills path)
- set `SKILL_TARGET_DIR` to explicitly override either default

Optional flags:

```bash
# overwrite existing matching assets (after backup)
./scripts/install_codex_helper.sh --force

# append global guidance block into ~/.codex/AGENTS.md
./scripts/install_codex_helper.sh --with-global-guidance

# preview operations without writing
./scripts/install_codex_helper.sh --dry-run
```

## Symlink method (power users)

Use symlinks so updates in this repo immediately reflect in local Codex paths:

```bash
./scripts/link_codex_helper.sh
```

## Obsidian bundle export

```bash
./scripts/export_obsidian_bundle.sh "/path/to/ObsidianVault"
# overwrite existing exported bundle
./scripts/export_obsidian_bundle.sh --force "/path/to/ObsidianVault"
```

## Manual method

1. Resolve install targets:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
if [ -n "${SKILL_TARGET_DIR:-}" ]; then
  RESOLVED_SKILL_TARGET_DIR="$SKILL_TARGET_DIR"
elif [ -d "$CODEX_HOME/skills" ]; then
  RESOLVED_SKILL_TARGET_DIR="$CODEX_HOME/skills"
else
  RESOLVED_SKILL_TARGET_DIR="$HOME/.agents/skills"
fi
echo "Using skill target: $RESOLVED_SKILL_TARGET_DIR"
```

2. Create target folders if missing:

```bash
mkdir -p "$CODEX_HOME/agents"
mkdir -p "$RESOLVED_SKILL_TARGET_DIR"
```

3. Copy custom agents:

```bash
cp .codex/agents/*.toml "$CODEX_HOME/agents/"
```

4. Copy custom skills:

```bash
cp -R .agents/skills/* "$RESOLVED_SKILL_TARGET_DIR/"
```

5. Copy config template:

```bash
cp .codex/config.toml "$CODEX_HOME/config.codex-helper.example.toml"
```

6. Optional: append global guidance block from `templates/global-AGENTS.md` into `~/.codex/AGENTS.md`.

## Verify installation

```bash
ls "$CODEX_HOME/agents"
ls "$RESOLVED_SKILL_TARGET_DIR"
codex --version
```

## Notes

- Existing files are backed up before overwrite operations when using `--force`.
- `--with-global-guidance` appends a marked block so it can be removed cleanly later.
