# Canonical Skill: meeting-notes-and-actions

Generated at: `2026-03-18T08:06:29+00:00`
Translation status: `english`
Canonical ID: `skill--meeting-notes-and-actions`

## Summary
Turn meeting transcripts or rough notes into crisp summaries with decisions, risks, and owner-tagged action items; use for Zoom/Meet/Teams transcripts, call notes, or long meeting chats to generate share-ready outputs.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `meeting-notes-and-actions/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/meeting-notes-and-actions/SKILL.md))

## Metadata
- Tags: `meeting-notes-and-actions, skill, skill-md`
- Languages: ``
- Systems: ``
- Jobs: `meeting-notes-and-actions, skill-md`
- Roles: ``

## Steps
1. Action items: who/what/when. Convert vague asks into concrete tasks; propose due dates if missing.
2. Extract essentials: agenda topics, key decisions, open questions, risks/blocked items.
3. Header with meeting title, date, attendees.
4. Include timeline of major moments if timestamps exist.
5. Normalize text: strip timestamps/speaker labels if noisy; lightly clean filler words; keep quoted statements intact.
6. Output style: terse bullets vs. narrative, action-item format, due date/owner tags, redaction rules if any.
7. Produce output:
8. Provide short Slack/Email-ready blurb (2–3 sentences) plus the full notes.
9. Quality checks: ensure names are consistent; no hallucinated facts; flag ambiguities as clarifying questions.
10. Sections: `Summary`, `Decisions`, `Open Questions/Risks`, `Action Items` (checkboxes with owner + due).
11. Source: pasted transcript/text or file path; meeting title/date; attendees and their handles.

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: meeting-notes-and-actions/SKILL.md
# Meeting Notes & Actions

Process transcripts into structured notes and action items.

## Inputs to ask for
- Source: pasted transcript/text or file path; meeting title/date; attendees and their handles.
- Output style: terse bullets vs. narrative, action-item format, due date/owner tags, redaction rules if any.

## Workflow
1) Normalize text: strip timestamps/speaker labels if noisy; lightly clean filler words; keep quoted statements intact.
2) Extract essentials: agenda topics, key decisions, open questions, risks/blocked items.
3) Action items: who/what/when. Convert vague asks into concrete tasks; propose due dates if missing.
4) Produce output:
   - Header with meeting title, date, attendees.
   - Sections: `Summary`, `Decisions`, `Open Questions/Risks`, `Action Items` (checkboxes with owner + due).
5) Quality checks: ensure names are consistent; no hallucinated facts; flag ambiguities as clarifying questions.

## Optional extras
- Include timeline of major moments if timestamps exist.
- Provide short Slack/Email-ready blurb (2–3 sentences) plus the full notes.
