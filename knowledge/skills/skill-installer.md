# Canonical Skill: skill-installer

Generated at: `2026-03-18T09:12:23+00:00`
Translation status: `english`
Canonical ID: `skill--skill-installer`

## Summary
Install Codex skills into $CODEX_HOME/skills from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, or install a skill from another repo (including private repos).

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `skill-installer/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/skill-installer/SKILL.md))

## Metadata
- Tags: `skill, skill-installer, skill-md`
- Languages: `c`
- Systems: `git, github`
- Jobs: `skill-installer, skill-md`
- Roles: ``

## Steps
1. ...
2. Aborts if the destination skill directory already exists.
3. Curated listing is fetched from `https://github.com/openai/skills/tree/main/skills/.curated` via the GitHub API. If it is unavailable, explain the error and exit.
4. Defaults to direct download for public GitHub repos.
5. Git fallback tries HTTPS first, then SSH.
6. If download fails with auth/permission errors, falls back to git sparse checkout.
7. Install from another repo when the user provides a GitHub repo/path (including private repos).
8. Install from the curated list when the user provides a skill name.
9. Installs into `$CODEX_HOME/skills/<skill-name>` (defaults to `~/.codex/skills`).
10. List curated skills when the user asks what is available, or if the user uses this skill without specifying what to do.
11. Multiple `--path` values install multiple skills in one run, each named from the path basename unless `--name` is supplied.
12. Options: `--ref <ref>` (default `main`), `--dest <path>`, `--method auto|download|git`.
13. Private GitHub repos can be accessed via existing git credentials or optional `GITHUB_TOKEN`/`GH_TOKEN` for download.
14. The skills at https://github.com/openai/skills/tree/main/skills/.system are preinstalled, so no need to help users install those. If they ask, just explain this. If they insist, you can download and overwrite.
15. `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
16. `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`
17. `scripts/list-curated-skills.py --format json`
18. `scripts/list-curated-skills.py` (prints curated list with installed annotations)
19. skill-1
20. skill-2 (already installed)

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: skill-installer/SKILL.md
# Skill Installer

Helps install skills. By default these are from https://github.com/openai/skills/tree/main/skills/.curated, but users can also provide other locations.

Use the helper scripts based on the task:
- List curated skills when the user asks what is available, or if the user uses this skill without specifying what to do.
- Install from the curated list when the user provides a skill name.
- Install from another repo when the user provides a GitHub repo/path (including private repos).

Install skills with the helper scripts.

## Communication

When listing curated skills, output approximately as follows, depending on the context of the user's request:
"""
Skills from {repo}:
1. skill-1
2. skill-2 (already installed)
3. ...
Which ones would you like installed?
"""

After installing a skill, tell the user: "Restart Codex to pick up new skills."

## Scripts

All of these scripts use network, so when running in the sandbox, request escalation when running them.

- `scripts/list-curated-skills.py` (prints curated list with installed annotations)
- `scripts/list-curated-skills.py --format json`
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`

## Behavior and Options

- Defaults to direct download for public GitHub repos.
- If download fails with auth/permission errors, falls back to git sparse checkout.
- Aborts if the destination skill directory already exists.
- Installs into `$CODEX_HOME/skills/<skill-name>` (defaults to `~/.codex/skills`).
- Multiple `--path` values install multiple skills in one run, each named from the path basename unless `--name` is supplied.
- Options: `--ref <ref>` (default `main`), `--dest <path>`, `--method auto|download|git`.

## Notes

- Curated listing is fetched from `https://github.com/openai/skills/tree/main/skills/.curated` via the GitHub API. If it is unavailable, explain the error and exit.
- Private GitHub repos can be accessed via existing git credentials or optional `GITHUB_TOKEN`/`GH_TOKEN` for download.
- Git fallback tries HTTPS first, then SSH.
- The skills at https://github.com/openai/skills/tree/main/skills/.system are preinstalled, so no need to help users install those. If they ask, just explain this. If they insist, you can download and overwrite.
- Installed annotations come from `$CODEX_HOME/skills`.
