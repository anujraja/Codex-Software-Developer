# Canonical Skill: github

Generated at: `2026-03-18T08:06:29+00:00`
Translation status: `english`
Canonical ID: `skill--github`

## Summary
Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries. Use when the user asks about GitHub issues, pull requests, workflows, or wants to interact with GitHub repositories from the command line — including tasks like check CI status, create PR, list issues, or query the GitHub API.

## Provenance
- `Dimillian/Skills` `main` `github/SKILL.md` ([raw](https://raw.githubusercontent.com/Dimillian/Skills/main/github/SKILL.md))

## Metadata
- Tags: `github, skill, skill-md`
- Languages: `sql`
- Systems: `git, github`
- Jobs: `github, skill-md`
- Roles: ``

## Steps
1. **Check PR status** — identify which checks are failing:
2. **Fetch failure logs** — get the detailed output for failed steps:
3. **List recent runs** — find the relevant run ID:
4. **View the failed run** — see which jobs and steps failed:

## Instructions
Source: Dimillian/Skills (main) :: github/SKILL.md
# GitHub Skill

Use the `gh` CLI to interact with GitHub. Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

## Pull Requests

Check CI status on a PR:
```bash
gh pr checks 55 --repo owner/repo
```

List recent workflow runs:
```bash
gh run list --repo owner/repo --limit 10
```

View a run and see which steps failed:
```bash
gh run view <run-id> --repo owner/repo
```

View logs for failed steps only:
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

### Debugging a CI Failure

Follow this sequence to investigate a failing CI run:

1. **Check PR status** — identify which checks are failing:
   ```bash
   gh pr checks 55 --repo owner/repo
   ```
2. **List recent runs** — find the relevant run ID:
   ```bash
   gh run list --repo owner/repo --limit 10
   ```
3. **View the failed run** — see which jobs and steps failed:
   ```bash
   gh run view <run-id> --repo owner/repo
   ```
4. **Fetch failure logs** — get the detailed output for failed steps:
   ```bash
   gh run view <run-id> --repo owner/repo --log-failed
   ```

## API for Advanced Queries

The `gh api` command is useful for accessing data not available through other subcommands.

Get PR with specific fields:
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON Output

Most commands support `--json` for structured output.  You can use `--jq` to filter:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```
