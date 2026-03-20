# Canonical Skill: prompt-optimization

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--prompt-optimization`

## Summary
Improve and rewrite user prompts to reduce ambiguity and improve LLM output quality. Use when a user asks to optimize, refine, clarify, or rewrite a prompt for better results, or when the request is about prompt optimization or prompt rewriting.

## Provenance
- `proflead/codex-skills-library` `master` `.codex/skills/prompt-optimization/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/.codex/skills/prompt-optimization/SKILL.md))

## Metadata
- Tags: `codex, prompt-optimization, skill, skills`
- Languages: `c`
- Systems: ``
- Jobs: `codex, skills`
- Roles: ``

## Steps
1. $automating-productivity
2. Add relevant constraints (format, length, style) when helpful.
3. Do not assume domain knowledge not in the original prompt.
4. Identify ambiguity, missing context, or unclear intent.
5. Improved prompt
6. Preserve user intent.
7. Read the user's original prompt carefully.
8. Retain the core intention of the user's request.
9. Rewrite the prompt to remove ambiguity and provide clear instructions.
10. Short explanation of what was improved
11. “Draft me an email asking for feedback.”
12. “Turn this into a daily to-do list.”

## Instructions
Source: proflead/codex-skills-library (master) :: .codex/skills/prompt-optimization/SKILL.md
# Prompt Optimization

## Goal

Improve the user's prompt so Codex (or any LLM) produces better output while preserving intent.

## Workflow

1. Read the user's original prompt carefully.
2. Identify ambiguity, missing context, or unclear intent.
3. Rewrite the prompt to remove ambiguity and provide clear instructions.
4. Retain the core intention of the user's request.
5. Add relevant constraints (format, length, style) when helpful.

## Output format

Provide:
- Improved prompt
- Short explanation of what was improved

## Constraints

- Do not assume domain knowledge not in the original prompt.
- Preserve user intent.

## Example triggers
- “Draft me an email asking for feedback.”
- “Turn this into a daily to-do list.”
- $automating-productivity
