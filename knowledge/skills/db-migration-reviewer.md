# Canonical Skill: db-migration-reviewer

Generated at: `2026-03-18T09:12:23+00:00`
Translation status: `english`
Canonical ID: `skill--db-migration-reviewer`

## Summary
Review database migrations for safety and rollback. Use when a mid-level developer needs validation of schema changes.

## Provenance
- `proflead/codex-skills-library` `master` `skills/data/db-migration-reviewer/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/data/db-migration-reviewer/SKILL.md))

## Metadata
- Tags: `data, db-migration-reviewer, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `data, skills`
- Roles: `reviewer`

## Steps
1. Call out data loss risks explicitly.
2. Check for locks, long-running operations, and data backfills.
3. Confirm migration order and dependency handling.
4. Database size and traffic patterns.
5. Ensure forward and rollback paths are defined.
6. Flag operations that lock large tables.
7. Migration risks and recommended changes.
8. Migration scripts and execution order.
9. Rollback strategy and downtime tolerance.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/data/db-migration-reviewer/SKILL.md
# DB Migration Reviewer

## Purpose
Review database migrations for safety and rollback.

## Inputs to request
- Migration scripts and execution order.
- Database size and traffic patterns.
- Rollback strategy and downtime tolerance.

## Workflow
1. Check for locks, long-running operations, and data backfills.
2. Ensure forward and rollback paths are defined.
3. Confirm migration order and dependency handling.

## Output
- Migration risks and recommended changes.

## Quality bar
- Flag operations that lock large tables.
- Call out data loss risks explicitly.
