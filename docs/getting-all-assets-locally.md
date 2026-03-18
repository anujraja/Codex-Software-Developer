# Get All Agents And Skills Locally

This guide gives both script-based and manual installation methods.

## Script method (recommended)

From this repo root:

```bash
./scripts/install_codex_helper.sh
```

Default install behavior:
- installs canonical catalog agents from `knowledge/agents/*.toml`
- installs canonical catalog skills from `knowledge/skills/*.md` into `SKILL.md` wrappers
- installs custom overlay agents from `.codex/agents/*.toml`
- installs custom overlay skills from `.agents/skills/*`
- custom overlay wins on name collisions

Skill target default behavior:
- if `~/.codex/skills` already exists, scripts install/link skills there
- otherwise scripts use `~/.agents/skills` (official Codex docs user-level skills path)
- set `SKILL_TARGET_DIR` to explicitly override either default

Optional flags:

```bash
# overwrite existing matching assets (after backup)
./scripts/install_codex_helper.sh --force

# create/update global guidance block in ~/.codex/AGENTS.md
./scripts/install_codex_helper.sh --with-global-guidance

# install only custom overlay assets
./scripts/install_codex_helper.sh --custom-only

# install only canonical catalog assets
./scripts/install_codex_helper.sh --catalog-only

# preview operations without writing
./scripts/install_codex_helper.sh --dry-run
```

## Symlink method (power users)

Use symlinks so updates in this repo reflect in local Codex paths:

```bash
./scripts/link_codex_helper.sh
```

Optional flags:

```bash
# force replace existing targets
./scripts/link_codex_helper.sh --force

# only custom overlay assets
./scripts/link_codex_helper.sh --custom-only

# only canonical catalog assets
./scripts/link_codex_helper.sh --catalog-only

# preview without writing
./scripts/link_codex_helper.sh --dry-run
```

Notes:
- catalog skills are linked via generated wrappers under `~/.codex/tmp/codex-helper-skill-link-cache`
- custom skills stay as direct symlinks to `.agents/skills/*`

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

3. Copy agents:

```bash
cp .codex/agents/*.toml "$CODEX_HOME/agents/"
cp knowledge/agents/*.toml "$CODEX_HOME/agents/"
```

4. Copy custom skills:

```bash
cp -R .agents/skills/* "$RESOLVED_SKILL_TARGET_DIR/"
```

5. Convert canonical skill markdown into Codex `SKILL.md` folders:

```bash
for src in knowledge/skills/*.md; do
  skill_name="$(basename "$src" .md)"
  dst_dir="$RESOLVED_SKILL_TARGET_DIR/$skill_name"
  mkdir -p "$dst_dir"
  summary="$(awk '/^## Summary/{getline; print; exit}' "$src")"
  [ -z "$summary" ] && summary="Imported canonical skill from Codex Helper knowledge catalog."
  {
    printf -- '---\n'
    printf 'name: %s\n' "$skill_name"
    printf 'description: >-\n'
    printf '  %s\n' "$summary"
    printf -- '---\n\n'
    cat "$src"
    printf '\n'
  } > "$dst_dir/SKILL.md"
done
```

6. Copy config template:

```bash
cp .codex/config.toml "$CODEX_HOME/config.codex-helper.example.toml"
```

7. Optional: create or refresh the guidance block from `templates/global-AGENTS.md` into `~/.codex/AGENTS.md`.

## Verify installation

```bash
ls "$CODEX_HOME/agents"
ls "$RESOLVED_SKILL_TARGET_DIR"
codex --version
```

## Notes

- Existing files are backed up before overwrite operations when using `--force`.
- `--with-global-guidance` creates or refreshes the marked block so routing guidance stays current.
