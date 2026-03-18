# Canonical Skill: iac-reviewer

Generated at: `2026-03-18T08:06:29+00:00`
Translation status: `english`
Canonical ID: `skill--iac-reviewer`

## Summary
Review infrastructure-as-code changes for safety and correctness. Use when a mid-level developer needs a second look on IaC.

## Provenance
- `proflead/codex-skills-library` `master` `skills/infra/iac-reviewer/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/infra/iac-reviewer/SKILL.md))

## Metadata
- Tags: `iac-reviewer, infra, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `infra, skills`
- Roles: `reviewer`

## Steps
1. Check resource changes for drift and deletion risk.
2. Confirm least-privilege IAM changes.
3. Confirm plan/apply order and state handling.
4. Flag destructive changes clearly.
5. IaC plan output or diff.
6. IaC review findings with risks.
7. Rollback or drift policy.
8. Target environments and accounts.
9. Validate security groups, IAM, and networking rules.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/infra/iac-reviewer/SKILL.md
# IaC Reviewer

## Purpose
Review infrastructure-as-code changes for safety and correctness.

## Inputs to request
- IaC plan output or diff.
- Target environments and accounts.
- Rollback or drift policy.

## Workflow
1. Check resource changes for drift and deletion risk.
2. Validate security groups, IAM, and networking rules.
3. Confirm plan/apply order and state handling.

## Output
- IaC review findings with risks.

## Quality bar
- Flag destructive changes clearly.
- Confirm least-privilege IAM changes.
