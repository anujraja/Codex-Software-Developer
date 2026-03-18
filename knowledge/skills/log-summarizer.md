# Canonical Skill: log-summarizer

Generated at: `2026-03-18T08:03:51+00:00`
Translation status: `english`
Canonical ID: `skill--log-summarizer`

## Summary
Summarize noisy logs into likely causes and next steps. Use when a junior developer needs help interpreting logs.

## Provenance
- `proflead/codex-skills-library` `master` `skills/foundation/log-summarizer/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/foundation/log-summarizer/SKILL.md))

## Metadata
- Tags: `foundation, log-summarizer, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `foundation, skills`
- Roles: ``

## Steps
1. Focus on the earliest failing signal.
2. Group similar errors and identify the first failure.
3. Likely root cause and next actions.
4. Log snippet and time range.
5. Recent deploys or config changes.
6. Separate symptoms from root causes.
7. Service or component name.
8. Suggest immediate checks or fixes.
9. Top error groups with counts.
10. Translate error messages into likely causes.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/foundation/log-summarizer/SKILL.md
# Log Summarizer

## Purpose
Summarize noisy logs into likely causes and next steps.

## Inputs to request
- Log snippet and time range.
- Service or component name.
- Recent deploys or config changes.

## Workflow
1. Group similar errors and identify the first failure.
2. Translate error messages into likely causes.
3. Suggest immediate checks or fixes.

## Output
- Top error groups with counts.
- Likely root cause and next actions.

## Quality bar
- Focus on the earliest failing signal.
- Separate symptoms from root causes.
