# Skill And Agent Routing Playbook

Use this when deciding what Codex should use first.

## Routing matrix

| Scenario | First choice | Optional follow-up |
|---|---|---|
| New repo onboarding | `explorer` | `docs_researcher` for external docs checks |
| Install or migrate Codex setup | `codex-install-assistant` | `implementation_worker` for script edits |
| Obsidian knowledge map updates | `obsidian-vault-map` | `implementation_worker` for content generation scripts |
| High-risk code review | `reviewer` | `explorer` for deep evidence gathering |
| Feature implementation | `implementation_worker` | `reviewer` before merge |
| Release prep | `release-audit` | `reviewer` for correctness regression pass |

## Practical rules

- Start read-only (`explorer`) when context is unclear.
- Use custom skills when task is operationally repetitive.
- Keep subagent scopes narrow and file ownership explicit.
- Use `reviewer` before pushing meaningful setup/runtime changes.
