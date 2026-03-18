# OpenAI Codex Notes (Verified 2026-03-18)

This file captures the specific official-doc points used to shape this repo.

## Core confirmations

- Codex CLI install command is `npm i -g @openai/codex`.
- Codex CLI docs confirm first run prompts sign-in and support ChatGPT account or API key.
- Current model guidance in Codex models docs says to start with `gpt-5.4` for most tasks and use `gpt-5.4-mini` for faster/lower-cost tasks.
- Skills docs use `~/.agents/skills` for user-level skills and `.agents/skills` for project-level skills.
- This repo's install/link scripts intentionally support a compatibility behavior: if `~/.codex/skills` already exists, that path is used by default; otherwise they fall back to `~/.agents/skills`.
- Subagents docs use `~/.codex/agents` for user-level custom agents and `.codex/agents` for project-level agents.
- AGENTS docs describe layered instruction discovery (`~/.codex/AGENTS.md`, repo `AGENTS.md`, and parent traversal).

## Official sources

- <https://developers.openai.com/codex>
- <https://developers.openai.com/codex/cli>
- <https://developers.openai.com/codex/models>
- <https://developers.openai.com/codex/skills>
- <https://developers.openai.com/codex/subagents>
- <https://developers.openai.com/codex/agents-md>
- <https://developers.openai.com/codex/config-basic>
- <https://github.com/openai/codex>

## Update policy

When changing setup docs or scripts in this repo:
1. re-check the above pages
2. update this file's date
3. adjust commands/paths in all linked docs
