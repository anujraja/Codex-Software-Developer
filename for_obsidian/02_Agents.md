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

## Full catalog

Use [[11_Capability_Catalog]] and [[catalog/01_Agents_Full]] for the complete generated list of every available agent profile.
Use [[graph/maps/by-role]] and [[graph/maps/by-system]] to explore connected agent clusters.

## Custom local agents in this repo

| Agent name | File | Focus |
|---|---|---|
| `reviewer` | `.codex/agents/reviewer.toml` | Correctness, risk, regressions, missing tests. |
| `docs_researcher` | `.codex/agents/docs_researcher.toml` | Source-backed documentation and setup validation. |
| `implementation_worker` | `.codex/agents/implementation_worker.toml` | Scoped implementation plus verification. |

## Linked views

- [[03_Skills]]
- [[04_Domains]]
- [[06_Decision_Guide]]
- [[11_Capability_Catalog]]
