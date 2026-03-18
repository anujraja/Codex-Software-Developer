# Canonical Skill: spreadsheet-formula-helper

Generated at: `2026-03-18T08:03:51+00:00`
Translation status: `english`
Canonical ID: `skill--spreadsheet-formula-helper`

## Summary
Write and debug spreadsheet formulas (Excel/Google Sheets), pivot tables, and array formulas; translate between dialects; use when users need working formulas with examples and edge-case checks.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `spreadsheet-formula-helper/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/spreadsheet-formula-helper/SKILL.md))

## Metadata
- Tags: `skill, skill-md, spreadsheet-formula-helper`
- Languages: ``
- Systems: ``
- Jobs: `skill-md, spreadsheet-formula-helper`
- Roles: ``

## Steps
1. Draft formula(s); when dynamic arrays are available, prefer them over copy-down formulas.
2. Edge cases: blank rows, mixed types, timezone/date quirks, duplicates; offer guardrails (e.g., `IFERROR`, `LET`, `LAMBDA`).
3. Explain how it works and where to place it; include named ranges if helpful.
4. Optional: quick troubleshooting checklist for common errors.
5. Platform (Excel/Sheets), locale (comma vs. semicolon separators), sample data layout (headers, ranges), expected outputs, and constraints (volatile functions allowed?).
6. Primary formula, short explanation, and a 2–3 row worked example showing inputs → outputs.
7. Provide small example rows and the desired result for them.
8. Restate the problem with explicit ranges and sheet names; propose a minimal sample to verify.
9. Variants: if porting between Excel and Sheets, provide both versions.

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: spreadsheet-formula-helper/SKILL.md
# Spreadsheet Formula Helper

Produce reliable spreadsheet formulas with explanations.

## Inputs to gather
- Platform (Excel/Sheets), locale (comma vs. semicolon separators), sample data layout (headers, ranges), expected outputs, and constraints (volatile functions allowed?).
- Provide small example rows and the desired result for them.

## Workflow
1) Restate the problem with explicit ranges and sheet names; propose a minimal sample to verify.
2) Draft formula(s); when dynamic arrays are available, prefer them over copy-down formulas.
3) Explain how it works and where to place it; include named ranges if helpful.
4) Edge cases: blank rows, mixed types, timezone/date quirks, duplicates; offer guardrails (e.g., `IFERROR`, `LET`, `LAMBDA`).
5) Variants: if porting between Excel and Sheets, provide both versions.

## Output
- Primary formula, short explanation, and a 2–3 row worked example showing inputs → outputs.
- Optional: quick troubleshooting checklist for common errors.
