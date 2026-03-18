# Canonical Skill: ci-failure-triage

Generated at: `2026-03-18T09:12:23+00:00`
Translation status: `english`
Canonical ID: `skill--ci-failure-triage`

## Summary
Diagnose CI failures and stabilize pipelines. Use when a mid-level developer needs to resolve flaky or failing builds.

## Provenance
- `proflead/codex-skills-library` `master` `skills/infra/ci-failure-triage/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/infra/ci-failure-triage/SKILL.md))

## Metadata
- Tags: `ci-failure-triage, infra, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `infra, skills`
- Roles: ``

## Steps
1. CI logs and failing jobs.
2. Check for environment changes and test flakiness.
3. Classify failures by stage and error type.
4. Flake frequency and patterns.
5. Prefer fixes that reduce future noise.
6. Propose fixes and temporary mitigations.
7. Recent merges and environment changes.
8. Separate flake from deterministic failure.
9. Triage summary with root cause candidates.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/infra/ci-failure-triage/SKILL.md
# CI Failure Triage

## Purpose
Diagnose CI failures and stabilize pipelines.

## Inputs to request
- CI logs and failing jobs.
- Recent merges and environment changes.
- Flake frequency and patterns.

## Workflow
1. Classify failures by stage and error type.
2. Check for environment changes and test flakiness.
3. Propose fixes and temporary mitigations.

## Output
- Triage summary with root cause candidates.

## Quality bar
- Separate flake from deterministic failure.
- Prefer fixes that reduce future noise.
