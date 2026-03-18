# Canonical Skill: context7

Generated at: `2026-03-18T08:06:29+00:00`
Translation status: `english`
Canonical ID: `skill--context7`

## Summary
|

## Provenance
- `am-will/codex-skills` `main` `skills/context7/SKILL.md` ([raw](https://raw.githubusercontent.com/am-will/codex-skills/main/skills/context7/SKILL.md))

## Metadata
- Tags: `context7, skill, skills`
- Languages: `c, javascript, react`
- Systems: ``
- Jobs: `context7, skills`
- Roles: ``

## Steps
1. Before implementing any library-dependent feature
2. For library version-specific behavior
3. To verify best practices and patterns
4. When unsure about current API signatures
5. `--tokens N` - Limit response tokens
6. `--type txt|md` - Output format (default: txt)

## Instructions
Source: am-will/codex-skills (main) :: skills/context7/SKILL.md
# Context7 Documentation Fetcher

Retrieve current library documentation via Context7 API.

IMPORTANT: `CONTEXT7_API_KEY` IS STORED IN THE .env FILE IN THE SKILL FOLDER THAT THE CONTEXT7 SKILL IS INSTALLED IN. SEARCH FOR IT THERE. .env FILES ARE HIDDEN FILES. 

Example: 
~/.agents/skills/context7/.env
~/.claude/skills/context7/.env

## Workflow

### 1. Search for the library

```bash
python3 ~/.codex/skills/context7/scripts/context7.py search "<library-name>"
```

Example:
```bash
python3 ~/.codex/skills/context7/scripts/context7.py search "next.js"
```

Returns library metadata including the `id` field needed for step 2.

### 2. Fetch documentation context

```bash
python3 ~/.codex/skills/context7/scripts/context7.py context "<library-id>" "<query>"
```

Example:
```bash
python3 ~/.codex/skills/context7/scripts/context7.py context "/vercel/next.js" "app router middleware"
```

Options:
- `--type txt|md` - Output format (default: txt)
- `--tokens N` - Limit response tokens

## Quick Reference

| Task | Command |
|------|---------|
| Find React docs | `search "react"` |
| Get React hooks info | `context "/facebook/react" "useEffect cleanup"` |
| Find Supabase | `search "supabase"` |
| Get Supabase auth | `context "/supabase/supabase" "authentication row level security"` |

## When to Use

- Before implementing any library-dependent feature
- When unsure about current API signatures
- For library version-specific behavior
- To verify best practices and patterns
