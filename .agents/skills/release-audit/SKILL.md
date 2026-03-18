---
name: release-audit
description: Use for release readiness checks, risk review, and documentation completeness before pushing.
---

# Release Audit

## Use this skill when
- someone asks to prepare a repo for push/release
- changes include scripts, setup docs, or operational workflows
- there is risk of regressions due to configuration changes

## Workflow

1. Verify scripts are executable and documented.
2. Verify docs match actual file paths and commands.
3. Verify critical onboarding docs exist (README, install guide, routing guide).
4. Verify cross-links in Obsidian notes are coherent.
5. Provide a short risk register.

## Output contract

Return:
- pass/fail checks
- unresolved risks
- exact next fixes required before push
