# Canonical Skill: error-message-explainer

Generated at: `2026-03-18T08:03:51+00:00`
Translation status: `english`
Canonical ID: `skill--error-message-explainer`

## Summary
Explain compiler/runtime errors in plain language. Use when a junior developer needs help understanding an error message.

## Provenance
- `proflead/codex-skills-library` `master` `skills/foundation/error-message-explainer/SKILL.md` ([raw](https://raw.githubusercontent.com/proflead/codex-skills-library/master/skills/foundation/error-message-explainer/SKILL.md))

## Metadata
- Tags: `error-message-explainer, foundation, skill, skills`
- Languages: ``
- Systems: ``
- Jobs: `foundation, skills`
- Roles: ``

## Steps
1. Cite the exact line or symbol if possible.
2. Code snippet around the failing line.
3. Fix suggestions with examples.
4. Full error text and stack trace.
5. Offer the smallest viable fix first.
6. Plain-language explanation.
7. Point to the most likely offending line or call.
8. Provide one or two possible fixes.
9. Restate the error in simple terms.
10. Runtime or compiler version.

## Instructions
Source: proflead/codex-skills-library (master) :: skills/foundation/error-message-explainer/SKILL.md
# Error Message Explainer

## Purpose
Explain compiler/runtime errors in plain language.

## Inputs to request
- Full error text and stack trace.
- Code snippet around the failing line.
- Runtime or compiler version.

## Workflow
1. Restate the error in simple terms.
2. Point to the most likely offending line or call.
3. Provide one or two possible fixes.

## Output
- Plain-language explanation.
- Fix suggestions with examples.

## Quality bar
- Cite the exact line or symbol if possible.
- Offer the smallest viable fix first.
