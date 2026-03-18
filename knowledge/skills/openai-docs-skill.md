# Canonical Skill: openai-docs-skill

Generated at: `2026-03-18T08:03:51+00:00`
Translation status: `english`
Canonical ID: `skill--openai-docs-skill`

## Summary
Query the OpenAI developer documentation via the OpenAI Docs MCP server using CLI (curl/jq). Use whenever a task involves the OpenAI API (Responses, Chat Completions, Realtime, etc.), OpenAI SDKs, ChatGPT Apps SDK, Codex, MCP integrations, endpoint schemas, parameters, limits, or migrations and you need up-to-date official guidance.

## Provenance
- `am-will/codex-skills` `main` `skills/openai-docs-skill/SKILL.md` ([raw](https://raw.githubusercontent.com/am-will/codex-skills/main/skills/openai-docs-skill/SKILL.md))

## Metadata
- Tags: `openai-docs-skill, skill, skills`
- Languages: `c, sql`
- Systems: `mcp`
- Jobs: `openai-docs-skill, skills`
- Roles: `developer`

## Steps
1. Always use this skill for OpenAI API/SDK/Apps/Codex questions or when precise, current docs are required.
2. Apply: summarize and/or quote relevant sections; include the URL.
3. Discover: `search` with a focused query. If unsure, use `list` to browse.
4. Query the MCP server via the CLI wrapper in `scripts/openai-docs-mcp.sh` (do not rely on Codex MCP tools).
5. Read: `fetch` the most relevant URL (optionally add an anchor).
6. Surface the doc URL you used in your response so sources are clear.
7. Use `search` or `list` to find the best doc page, then `fetch` the page (or anchor) for exact text.
8. `MCP_URL`: override the default MCP endpoint.
9. `endpoints`: list OpenAPI endpoints.
10. `fetch <url> [anchor]`: return markdown for a doc page or section.
11. `init`: initialize and inspect server capabilities.
12. `list [limit] [cursor]`: browse docs index.
13. `openapi <endpoint-url> [lang1,lang2] [code-only]`: fetch OpenAPI schema or code samples.
14. `search <query> [limit] [cursor]`: return JSON hits from the docs index.
15. `tools`: list available tools on the MCP server.

## Instructions
Source: am-will/codex-skills (main) :: skills/openai-docs-skill/SKILL.md
# OpenAI Docs MCP Skill

## Overview

Use the OpenAI developer documentation MCP server from the shell to search and fetch authoritative docs. Always do this for OpenAI platform work instead of relying on memory or non-official sources.

## Core rules

- Always use this skill for OpenAI API/SDK/Apps/Codex questions or when precise, current docs are required.
- Query the MCP server via the CLI wrapper in `scripts/openai-docs-mcp.sh` (do not rely on Codex MCP tools).
- Use `search` or `list` to find the best doc page, then `fetch` the page (or anchor) for exact text.
- Surface the doc URL you used in your response so sources are clear.

## Quick start

```bash
scripts/openai-docs-mcp.sh search "Responses API" 5
scripts/openai-docs-mcp.sh fetch https://platform.openai.com/docs/guides/migrate-to-responses
```

## Workflow

1. Discover: `search` with a focused query. If unsure, use `list` to browse.
2. Read: `fetch` the most relevant URL (optionally add an anchor).
3. Apply: summarize and/or quote relevant sections; include the URL.

## Script reference

The CLI wrapper is at `scripts/openai-docs-mcp.sh` and uses `curl` + `jq` against `https://developers.openai.com/mcp`.

Subcommands:
- `init`: initialize and inspect server capabilities.
- `tools`: list available tools on the MCP server.
- `search <query> [limit] [cursor]`: return JSON hits from the docs index.
- `list [limit] [cursor]`: browse docs index.
- `fetch <url> [anchor]`: return markdown for a doc page or section.
- `endpoints`: list OpenAPI endpoints.
- `openapi <endpoint-url> [lang1,lang2] [code-only]`: fetch OpenAPI schema or code samples.

Environment:
- `MCP_URL`: override the default MCP endpoint.
