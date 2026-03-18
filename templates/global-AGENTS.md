<!-- CODEX-HELPER START -->
## Codex Helper Global Guidance

- Prefer custom `reviewer` for risk-focused code review tasks.
- Prefer custom `docs_researcher` for docs-lookup and source-validation tasks.
- Prefer custom `implementation_worker` for bounded implementation tasks.
- Use `explorer` first when mapping unfamiliar codebases.
- Use custom skills in `~/.agents/skills/` when their task boundaries match.

### Quick routing

- Setup/install/sync -> `codex-install-assistant`
- Obsidian graph/docs map -> `obsidian-vault-map`
- Release readiness -> `release-audit`

### Guardrails

- Use non-destructive changes by default.
- Always summarize changed files and verification steps.
<!-- CODEX-HELPER END -->
