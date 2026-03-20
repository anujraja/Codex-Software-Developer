# Canonical Prompt: readme

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `prompt--readme`

## Summary
# Prompts This folder contains reusable prompt templates that pair with the skills and planning workflow in this repo. Use them as standalone instructions for coding agents, or copy them into your own tooling. ## File...

## Provenance
- `am-will/codex-skills` `main` `prompts/README.md` ([raw](https://raw.githubusercontent.com/am-will/codex-skills/main/prompts/README.md))

## Metadata
- Tags: `prompt, prompts, readme-md`
- Languages: ``
- Systems: ``
- Jobs: `prompts, readme-md`
- Roles: ``

## Steps
1. Best used before implementation work begins.
2. Customize wording or output templates to match your internal standards.
3. Emphasizes thorough context transfer and atomic scope per task.
4. General-purpose planning agent prompt.
5. Planning prompt intended for other coding agents to run **Codex xhigh** for planning.
6. Produces phased/sprint-based plans with atomic, committable tasks and clear validation steps.
7. Review and refine the plan.
8. Task orchestration prompt that reads a plan and delegates tasks to subagents (when available).
9. These prompts are designed to be repo-agnostic.
10. Use `prompts/parallel-task.md` to dispatch tasks for implementation.
11. Use `prompts/planner.md` (or `prompts/codex-plan.md` if you want Codex xhigh planning).
12. Use this to generate a high-quality plan in Codex, then hand that plan to another agent for implementation automatically.
13. `prompts/codex-plan.md`
14. `prompts/parallel-task.md`
15. `prompts/planner.md`

## Instructions
Source: am-will/codex-skills (main) :: prompts/README.md
# Prompts

This folder contains reusable prompt templates that pair with the skills and planning workflow in this repo. Use them as standalone instructions for coding agents, or copy them into your own tooling.

## Files

- `prompts/planner.md`
  - General-purpose planning agent prompt.
  - Produces phased/sprint-based plans with atomic, committable tasks and clear validation steps.
  - Best used before implementation work begins.

- `prompts/parallel-task.md`
  - Task orchestration prompt that reads a plan and delegates tasks to subagents (when available).
  - Emphasizes thorough context transfer and atomic scope per task.

- `prompts/codex-plan.md`
  - Planning prompt intended for other coding agents to run **Codex xhigh** for planning.
  - Use this to generate a high-quality plan in Codex, then hand that plan to another agent for implementation automatically.

## Suggested Workflow
1. Use `prompts/planner.md` (or `prompts/codex-plan.md` if you want Codex xhigh planning).
2. Review and refine the plan.
3. Use `prompts/parallel-task.md` to dispatch tasks for implementation.

## Notes
- These prompts are designed to be repo-agnostic.
- Customize wording or output templates to match your internal standards.
