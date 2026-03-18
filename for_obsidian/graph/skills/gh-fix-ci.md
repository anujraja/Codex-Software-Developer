---
tags: [codex, graph, skill]
---

# Skill Node: gh-fix-ci

Generated at: `2026-03-18T09:35:14+00:00`

## What this node does
Inspect GitHub PR checks with gh, pull failing GitHub Actions logs, summarize failure context, then create a fix plan and implement after user approval. Use when a user asks to debug or fix failing PR CI/CD checks on GitHub Actions and wants a plan + code changes; for external checks (e.g., Buildkite), only report the details URL and mark them out of scope.

## Connected roles
- none

## Connected systems
- [[graph/systems/git|git]]
- [[graph/systems/github|github]]

## Connected languages
- [[graph/languages/c|c]]

## Related agent nodes
- [[graph/agents/agents-config-block|agents-config-block]]
- [[graph/agents/devops-cicd-expert|devops-cicd-expert]]
- [[graph/agents/dotnet-architect|dotnet-architect]]
- [[graph/agents/dx-optimizer|dx-optimizer]]
- [[graph/agents/flutter-expert|flutter-expert]]
- [[graph/agents/frontend-developer|frontend-developer]]
- [[graph/agents/ml-data-expert|ml-data-expert]]
- [[graph/agents/ml-engineer|ml-engineer]]
- [[graph/agents/mlops-engineer|mlops-engineer]]
- [[graph/agents/posix-shell-pro|posix-shell-pro]]
- [[graph/agents/team-lead|team-lead]]
- [[graph/agents/agent-installer|agent-installer]]

## Related prompt nodes
- [[graph/prompts/codex-plan|codex-plan]]
- [[graph/prompts/github-default-prompt|github-default-prompt]]
- [[graph/prompts/skill|skill]]

## Linked views
- [[graph/00_Graph_Home]]
- [[11_Capability_Catalog]]
