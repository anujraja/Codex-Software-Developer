# Canonical Skill: cross-service-debugger

Generated at: `2026-03-18T08:06:29+00:00`
Translation status: `english`
Canonical ID: `skill--cross-service-debugger`

## Summary
Coordinate debugging across multiple services. Use when a senior developer needs to trace a distributed issue.

## Provenance
- `proflead/codex-skills-library` `master` `skills/infra/cross-service-debugger/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/infra/cross-service-debugger/SKILL.md))

## Metadata
- Tags: `cross-service-debugger, infra, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `infra, skills`
- Roles: ``

## Steps
1. Anchor analysis on a single request ID.
2. Correlate logs across services and time ranges.
3. Cross-service trace summary and next steps.
4. Distinguish upstream vs downstream errors.
5. Gather request IDs and trace context.
6. Isolate the failing hop and propose fixes.
7. Request IDs and trace context.
8. Service list and ownership.
9. Time window and environment.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/infra/cross-service-debugger/SKILL.md
# Cross-Service Debugger

## Purpose
Coordinate debugging across multiple services.

## Inputs to request
- Request IDs and trace context.
- Service list and ownership.
- Time window and environment.

## Workflow
1. Gather request IDs and trace context.
2. Correlate logs across services and time ranges.
3. Isolate the failing hop and propose fixes.

## Output
- Cross-service trace summary and next steps.

## Quality bar
- Anchor analysis on a single request ID.
- Distinguish upstream vs downstream errors.
