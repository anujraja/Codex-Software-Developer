# Canonical Skill: queue-processing-patterns

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--queue-processing-patterns`

## Summary
Design safe queue consumers and retries. Use when a mid-level developer needs reliable background processing.

## Provenance
- `proflead/codex-skills-library` `master` `skills/backend/queue-processing-patterns/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/backend/queue-processing-patterns/SKILL.md))

## Metadata
- Tags: `backend, queue-processing-patterns, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `backend, skills`
- Roles: ``

## Steps
1. Add metrics for lag and failure rates.
2. Define idempotency and retry policy.
3. Document poison message handling.
4. Ensure retries do not amplify failures.
5. Failure modes and retry limits.
6. Idempotency requirements.
7. Queue handling checklist.
8. Queue system and delivery semantics.
9. Set visibility timeout and dead-letter routing.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/backend/queue-processing-patterns/SKILL.md
# Queue Processing Patterns

## Purpose
Design safe queue consumers and retries.

## Inputs to request
- Queue system and delivery semantics.
- Idempotency requirements.
- Failure modes and retry limits.

## Workflow
1. Define idempotency and retry policy.
2. Set visibility timeout and dead-letter routing.
3. Add metrics for lag and failure rates.

## Output
- Queue handling checklist.

## Quality bar
- Ensure retries do not amplify failures.
- Document poison message handling.
