# Canonical Skill: notion-spec-to-implementation

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--notion-spec-to-implementation`

## Summary
Turn Notion specs into implementation plans, tasks, and progress tracking; use when implementing PRDs/feature specs and creating Notion plans + tasks from them.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `notion-spec-to-implementation/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/notion-spec-to-implementation/SKILL.md))

## Metadata
- Tags: `notion-spec-to-implementation, skill, skill-md`
- Languages: `c`
- Systems: `mcp, notion`
- Jobs: `notion-spec-to-implementation, skill-md`
- Roles: ``

## Steps
1. Add the Notion MCP:
2. Capture gaps/assumptions in a clarifications block before proceeding.
3. Create a plan page with `Notion:notion-create-pages` (pick a template: quick vs. full).
4. Create the plan via `Notion:notion-create-pages`, include: overview, linked spec, requirements summary, phases, dependencies/risks, and success criteria. Link back to the spec.
5. Enable remote MCP client:
6. Fetch the page (`Notion:notion-fetch`) and scan for requirements, acceptance criteria, constraints, and priorities. See `reference/spec-parsing.md` for extraction patterns.
7. Find the task database (`Notion:notion-search` → `Notion:notion-fetch` to confirm the data source and required properties). Patterns in `reference/task-creation.md`.
8. Find the task database, confirm schema, then create tasks with `Notion:notion-create-pages`.
9. Link spec ↔ plan ↔ tasks; keep status current with `Notion:notion-update-page`.
10. Locate the spec with `Notion:notion-search`, then fetch it with `Notion:notion-fetch`.
11. Log in with OAuth:
12. Multi-phase feature/migration → use `reference/standard-implementation-plan.md`.
13. Parse requirements and ambiguities using `reference/spec-parsing.md`.
14. Search first (`Notion:notion-search`); if multiple hits, ask the user which to use.
15. Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
16. Set properties: title/action verb, status, priority, relations to spec + plan, due date/story points/assignee if provided.
17. Simple change → use `reference/quick-implementation-plan.md`.
18. Size tasks to 1–2 days. Use `reference/task-creation-template.md` for content (context, objective, acceptance criteria, dependencies, resources).
19. `codex mcp add notion --url https://mcp.notion.com/mcp`
20. `codex mcp login notion`

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: notion-spec-to-implementation/SKILL.md
# Spec to Implementation

Convert a Notion spec into linked implementation plans, tasks, and ongoing status updates.

## Quick start
1) Locate the spec with `Notion:notion-search`, then fetch it with `Notion:notion-fetch`.
2) Parse requirements and ambiguities using `reference/spec-parsing.md`.
3) Create a plan page with `Notion:notion-create-pages` (pick a template: quick vs. full).
4) Find the task database, confirm schema, then create tasks with `Notion:notion-create-pages`.
5) Link spec ↔ plan ↔ tasks; keep status current with `Notion:notion-update-page`.

## Workflow

### 0) If any MCP call fails because Notion MCP is not connected, pause and set it up:
1. Add the Notion MCP:
   - `codex mcp add notion --url https://mcp.notion.com/mcp`
2. Enable remote MCP client:
   - Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Log in with OAuth:
   - `codex mcp login notion`

After successful login, the user will have to restart codex. You should finish your answer and tell them so when they try again they can continue with Step 1.

### 1) Locate and read the spec
- Search first (`Notion:notion-search`); if multiple hits, ask the user which to use.
- Fetch the page (`Notion:notion-fetch`) and scan for requirements, acceptance criteria, constraints, and priorities. See `reference/spec-parsing.md` for extraction patterns.
- Capture gaps/assumptions in a clarifications block before proceeding.

### 2) Choose plan depth
- Simple change → use `reference/quick-implementation-plan.md`.
- Multi-phase feature/migration → use `reference/standard-implementation-plan.md`.
- Create the plan via `Notion:notion-create-pages`, include: overview, linked spec, requirements summary, phases, dependencies/risks, and success criteria. Link back to the spec.

### 3) Create tasks
- Find the task database (`Notion:notion-search` → `Notion:notion-fetch` to confirm the data source and required properties). Patterns in `reference/task-creation.md`.
- Size tasks to 1–2 days. Use `reference/task-creation-template.md` for content (context, objective, acceptance criteria, dependencies, resources).
- Set properties: title/action verb, status, priority, relations to spec + plan, due date/story points/assignee if provided.
- Create pages with `Notion:notion-create-pages` using the database’s `data_source_id`.

### 4) Link artifacts
- Plan links to spec; tasks link to both plan and spec.
- Optionally update the spec with a short “Implementation” section pointing to the plan and tasks using `Notion:notion-update-page`.

### 5) Track progress
- Use the cadence in `reference/progress-tracking.md`.
- Post updates with `reference/progress-update-template.md`; close phases with `reference/milestone-summary-template.md`.
- Keep checklists and status fields in plan/tasks in sync; note blockers and decisions.

## References and examples
- `reference/` — parsing patterns, plan/task templates, progress cadence (e.g., `spec-parsing.md`, `standard-implementation-plan.md`, `task-creation.md`, `progress-tracking.md`).
- `examples/` — end-to-end walkthroughs (e.g., `ui-component.md`, `api-feature.md`, `database-migration.md`).
