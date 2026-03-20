# Canonical Skill: api-contract-checker

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--api-contract-checker`

## Summary
Validate API changes against an expected contract. Use when a mid-level developer needs to detect breaking changes.

## Provenance
- `proflead/codex-skills-library` `master` `skills/api/api-contract-checker/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/api/api-contract-checker/SKILL.md))

## Metadata
- Tags: `api, api-contract-checker, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `api, skills`
- Roles: ``

## Steps
1. Breaking change report with mitigation steps.
2. Compare endpoints, request/response fields, and status codes.
3. Flag any removal or behavior change clearly.
4. Identify breaking changes and backward-compatible adjustments.
5. Known consumers and usage patterns.
6. Old and new API specs or examples.
7. Recommend safe rollouts for clients.
8. Suggest versioning or migration notes.
9. Versioning policy and client expectations.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/api/api-contract-checker/SKILL.md
# API Contract Checker

## Purpose
Validate API changes against an expected contract.

## Inputs to request
- Old and new API specs or examples.
- Versioning policy and client expectations.
- Known consumers and usage patterns.

## Workflow
1. Compare endpoints, request/response fields, and status codes.
2. Identify breaking changes and backward-compatible adjustments.
3. Suggest versioning or migration notes.

## Output
- Breaking change report with mitigation steps.

## Quality bar
- Flag any removal or behavior change clearly.
- Recommend safe rollouts for clients.
