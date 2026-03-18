# Get All Agents And Skills Locally

This guide gives both script-based and manual installation methods.

## Script method (recommended)

From this repo root:

```bash
./scripts/install_codex_helper.sh
```

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

1. Create target folders if missing:

```bash
mkdir -p ~/.codex/agents
mkdir -p ~/.agents/skills
```

2. Copy custom agents:

```bash
cp .codex/agents/*.toml ~/.codex/agents/
```

3. Copy custom skills:

```bash
cp -R .agents/skills/* ~/.agents/skills/
```

4. Copy config template:

```bash
cp .codex/config.toml ~/.codex/config.codex-helper.example.toml
```

5. Optional: append global guidance block from `templates/global-AGENTS.md` into `~/.codex/AGENTS.md`.

## Verify installation

```bash
ls ~/.codex/agents
ls ~/.agents/skills
codex --version
```

## Notes

- Existing files are backed up before overwrite operations when using `--force`.
- `--with-global-guidance` appends a marked block so it can be removed cleanly later.
