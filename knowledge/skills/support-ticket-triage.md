# Canonical Skill: support-ticket-triage

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--support-ticket-triage`

## Summary
Triage customer support tickets/emails/chats into categories, priority, and next action; draft responses and create reproducible steps; use for Zendesk/Intercom/Help Scout exports or pasted threads.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `support-ticket-triage/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/support-ticket-triage/SKILL.md))

## Metadata
- Tags: `skill, skill-md, support-ticket-triage`
- Languages: ``
- Systems: ``
- Jobs: `skill-md, support-ticket-triage`
- Roles: ``

## Steps
1. Avoid promises; give ranges not exact ETAs unless provided.
2. Categorize: assign category and subcategory; set priority (e.g., P0–P3) with short justification.
3. Desired outputs: category taxonomy, priority levels, SLA hints, tone/brand voice, whether to draft a reply.
4. Draft response (if asked): concise acknowledgment, empathy, restate issue, next steps, and ask for missing info; include reproduction checklist when uncertain.
5. If signal is weak, present 2–3 likely categories and what evidence would disambiguate.
6. Internal notes: suspected root cause, logs to pull, teams to loop, and tracking IDs to create/attach.
7. Mask PII if copying to public channels.
8. Output: tabular or bullet summary with `Category`, `Priority`, `Summary`, `Proposed Fix/Next Steps`, `Reply Draft`.
9. Parse context: identify issue type, product surface, severity, customer impact, reproduction hints, and blockers.
10. Ticket text (include attachments/links), product area, customer plan/tier if known.

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: support-ticket-triage/SKILL.md
# Support Ticket Triage

Standardize how to classify and respond to incoming tickets.

## Inputs to gather
- Ticket text (include attachments/links), product area, customer plan/tier if known.
- Desired outputs: category taxonomy, priority levels, SLA hints, tone/brand voice, whether to draft a reply.

## Workflow
1) Parse context: identify issue type, product surface, severity, customer impact, reproduction hints, and blockers.
2) Categorize: assign category and subcategory; set priority (e.g., P0–P3) with short justification.
3) Draft response (if asked): concise acknowledgment, empathy, restate issue, next steps, and ask for missing info; include reproduction checklist when uncertain.
4) Internal notes: suspected root cause, logs to pull, teams to loop, and tracking IDs to create/attach.
5) Output: tabular or bullet summary with `Category`, `Priority`, `Summary`, `Proposed Fix/Next Steps`, `Reply Draft`.

## Quality checks
- Avoid promises; give ranges not exact ETAs unless provided.
- Mask PII if copying to public channels.
- If signal is weak, present 2–3 likely categories and what evidence would disambiguate.
