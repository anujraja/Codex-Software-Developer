---
tags: [codex, decision-guide]
---

# Decision Guide

## Quick decision table

| If your task is... | Use this first |
|---|---|
| Install or update local Codex setup | `codex-install-assistant` |
| Build/maintain Obsidian graph docs | `obsidian-vault-map` |
| Evaluate release risk before push | `release-audit` |
| Explore unfamiliar code without edits | `explorer` |
| Execute scoped code changes | `implementation_worker` |
| Validate external documentation quality | `docs_researcher` |
| Do a final correctness-oriented review | `reviewer` |
| Browse all available capability options | `11_Capability_Catalog` |

## Escalation path

1. Start with the smallest specialized skill or agent.
2. Move to `worker` only when write operations are needed.
3. Use `reviewer` before final push when changes affect scripts, config, or onboarding.
4. If you are unsure what exists, open [[11_Capability_Catalog]] and pick from full lists.
