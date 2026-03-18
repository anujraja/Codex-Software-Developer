# Canonical Skill: gh-address-comments

Generated at: `2026-03-18T09:12:23+00:00`
Translation status: `english`
Canonical ID: `skill--gh-address-comments`

## Summary
Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `gh-address-comments/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/gh-address-comments/SKILL.md))

## Metadata
- Tags: `gh-address-comments, skill, skill-md`
- Languages: ``
- Systems: `git, github`
- Jobs: `gh-address-comments, skill-md`
- Roles: ``

## Steps
1. Apply fixes for the selected comments
2. Ask the user which numbered comments should be addressed
3. If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
4. Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
5. Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: gh-address-comments/SKILL.md
# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
