# Canonical Skill: config-hardening

Generated at: `2026-03-18T08:03:51+00:00`
Translation status: `english`
Canonical ID: `skill--config-hardening`

## Summary
Harden configuration and defaults for safer deployment. Use when a mid-level developer needs to reduce misconfig risks.

## Provenance
- `proflead/codex-skills-library` `master` `skills/security/config-hardening/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/security/config-hardening/SKILL.md))

## Metadata
- Tags: `config-hardening, security, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `security, skills`
- Roles: ``

## Steps
1. Audit environment variables and defaults.
2. Avoid breaking changes without migration notes.
3. Call out secret handling explicitly.
4. Config hardening checklist.
5. Current configuration defaults.
6. Environment and deployment model.
7. Identify secrets and rotate if exposed.
8. Recommend safer defaults and validation.
9. Security requirements and threat model.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/security/config-hardening/SKILL.md
# Config Hardening

## Purpose
Harden configuration and defaults for safer deployment.

## Inputs to request
- Current configuration defaults.
- Environment and deployment model.
- Security requirements and threat model.

## Workflow
1. Audit environment variables and defaults.
2. Recommend safer defaults and validation.
3. Identify secrets and rotate if exposed.

## Output
- Config hardening checklist.

## Quality bar
- Avoid breaking changes without migration notes.
- Call out secret handling explicitly.
