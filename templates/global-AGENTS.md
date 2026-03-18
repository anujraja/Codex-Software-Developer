<!-- CODEX-HELPER START -->
## Codex Helper Global Guidance

- Prefer custom `reviewer` for risk-focused code review tasks.
- Prefer custom `docs_researcher` for docs-lookup and source-validation tasks.
- Prefer custom `implementation_worker` for bounded implementation tasks.
- Use `explorer` first when mapping unfamiliar codebases.
- Use custom skills from the active user skill path:
  - `~/.agents/skills/` (official docs path)
  - `~/.codex/skills/` (workspace-compatible path used by some setups)

### Quick routing

- Setup/install/sync -> `codex-install-assistant`
- Obsidian graph/docs map -> `obsidian-vault-map`
- Release readiness -> `release-audit`

### Guardrails

- Use non-destructive changes by default.
- Always summarize changed files and verification steps.

### Selection Policy

- Proactively choose the best-matching skill before implementation when a clear fit exists.
- Prefer installed skills from `~/.codex/skills/` and `~/.agents/skills/` based on task boundaries.
- For docs/source validation, prefer `docs_researcher`; for bounded implementation, prefer `implementation_worker`; for risk reviews, prefer `reviewer`.
- Use `explorer` first for unfamiliar codebases before making edits.
- If multiple skills/agents apply, use the smallest effective set in sequence.
<!-- CODEX-HELPER END -->
