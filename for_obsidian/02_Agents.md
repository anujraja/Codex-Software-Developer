---
tags: [codex, agents, roles]
---

# Agents

## Built-in role agents

| Agent | Role | When to use |
|---|---|---|
| `default` | General-purpose | Standard mixed tasks when no specialization is needed. |
| `explorer` | Read-only codebase exploration | Fast discovery, architecture tracing, evidence gathering. |
| `worker` | Execution and production work | Bounded implementation tasks with clear file ownership. |

## Custom agents in this repo

| Agent name | File | Focus |
|---|---|---|
| `reviewer` | `.codex/agents/reviewer.toml` | Correctness, risk, regressions, missing tests. |
| `docs_researcher` | `.codex/agents/docs_researcher.toml` | Source-backed documentation and setup validation. |
| `implementation_worker` | `.codex/agents/implementation_worker.toml` | Scoped implementation plus verification. |

## Linked views

- [[03_Skills]]
- [[04_Domains]]
- [[06_Decision_Guide]]
