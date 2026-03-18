# Canonical Skill: swiftui-performance-audit

Generated at: `2026-03-18T09:12:23+00:00`
Translation status: `english`
Canonical ID: `skill--swiftui-performance-audit`

## Summary
Audit and improve SwiftUI runtime performance from code review and architecture. Use for requests to diagnose slow rendering, janky scrolling, high CPU/memory usage, excessive view updates, or layout thrash in SwiftUI apps, and to provide guidance for user-run Instruments profiling when code review alone is insufficient.

## Provenance
- `Dimillian/Skills` `main` `swiftui-performance-audit/SKILL.md` ([raw](https://raw.githubusercontent.com/Dimillian/Skills/main/swiftui-performance-audit/SKILL.md))

## Metadata
- Tags: `skill, skill-md, swiftui-performance-audit`
- Languages: `swift`
- Systems: `ios`
- Jobs: `skill-md, swiftui-performance-audit`
- Roles: ``

## Steps
1. Animation or transition work applied too broadly.
2. CPU spike or battery drain
3. Classify the symptom: slow rendering, janky scrolling, high CPU, memory growth, hangs, or excessive view updates.
4. Data flow: `@State`, `@Binding`, environment dependencies, and observable models.
5. Excessive or unexpectedly broad view updates
6. Hangs or unresponsive interactions
7. Heavy derived work in `body` or view builders.
8. High memory or image pressure
9. If code is available, start with a code-first review using `references/code-smells.md`.
10. If code is not available, ask for the smallest useful slice: target view, data flow, reproduction steps, and deployment target.
11. If code review is inconclusive or runtime evidence is required, guide the user through profiling with `references/profiling-intake.md`.
12. Invalidation storms from broad observation or environment reads.
13. Janky scrolling or dropped frames
14. Large image decode or resize work on the main thread.
15. Layout thrash from complex hierarchies, `GeometryReader`, or preference chains.
16. Summarize likely causes, evidence, remediation, and validation steps using `references/report-template.md`.
17. Symptoms and exact reproduction steps.
18. Target view or feature code.
19. Unstable identity in lists and `ForEach`.
20. Whether the issue shows up on device or simulator, and whether it was observed in Debug or Release.

## Instructions
Source: Dimillian/Skills (main) :: swiftui-performance-audit/SKILL.md
# SwiftUI Performance Audit

## Quick start

Use this skill to diagnose SwiftUI performance issues from code first, then request profiling evidence when code review alone cannot explain the symptoms.

## Workflow

1. Classify the symptom: slow rendering, janky scrolling, high CPU, memory growth, hangs, or excessive view updates.
2. If code is available, start with a code-first review using `references/code-smells.md`.
3. If code is not available, ask for the smallest useful slice: target view, data flow, reproduction steps, and deployment target.
4. If code review is inconclusive or runtime evidence is required, guide the user through profiling with `references/profiling-intake.md`.
5. Summarize likely causes, evidence, remediation, and validation steps using `references/report-template.md`.

## 1. Intake

Collect:
- Target view or feature code.
- Symptoms and exact reproduction steps.
- Data flow: `@State`, `@Binding`, environment dependencies, and observable models.
- Whether the issue shows up on device or simulator, and whether it was observed in Debug or Release.

Ask the user to classify the issue if possible:
- CPU spike or battery drain
- Janky scrolling or dropped frames
- High memory or image pressure
- Hangs or unresponsive interactions
- Excessive or unexpectedly broad view updates

For the full profiling intake checklist, read `references/profiling-intake.md`.

## 2. Code-First Review

Focus on:
- Invalidation storms from broad observation or environment reads.
- Unstable identity in lists and `ForEach`.
- Heavy derived work in `body` or view builders.
- Layout thrash from complex hierarchies, `GeometryReader`, or preference chains.
- Large image decode or resize work on the main thread.
- Animation or transition work applied too broadly.

Use `references/code-smells.md` for the detailed smell catalog and fix guidance.

Provide:
- Likely root causes with code references.
- Suggested fixes and refactors.
- If needed, a minimal repro or instrumentation suggestion.

## 3. Guide the User to Profile

If code review does not explain the issue, ask for runtime evidence:
- A trace export or screenshots of the SwiftUI timeline and Time Profiler call tree.
- Device/OS/build configuration.
- The exact interaction being profiled.
- Before/after metrics if the user is comparing a change.

Use `references/profiling-intake.md` for the exact checklist and collection steps.

## 4. Analyze and Diagnose

- Map the evidence to the most likely category: invalidation, identity churn, layout thrash, main-thread work, image cost, or animation cost.
- Prioritize problems by impact, not by how easy they are to explain.
- Distinguish code-level suspicion from trace-backed evidence.
- Call out when profiling is still insufficient and what additional evidence would reduce uncertainty.

## 5. Remediate

Apply targeted fixes:
- Narrow state scope and reduce broad observation fan-out.
- Stabilize identities for `ForEach` and lists.
- Move heavy work out of `body` into derived state updated from inputs, model-layer precomputation, memoized helpers, or background preprocessing. Use `@State` only for view-owned state, not as an ad hoc cache for arbitrary computation.
- Use `equatable()` only when equality is cheaper than recomputing the subtree and the inputs are truly value-semantic.
- Downsample images before rendering.
- Reduce layout complexity or use fixed sizing where possible.

Use `references/code-smells.md` for examples, Observation-specific fan-out guidance, and remediation patterns.

## 6. Verify

Ask the user to re-run the same capture and compare with baseline metrics.
Summarize the delta (CPU, frame drops, memory peak) if provided.

## Outputs

Provide:
- A short metrics table (before/after if available).
- Top issues (ordered by impact).
- Proposed fixes with estimated effort.

Use `references/report-template.md` when formatting the final audit.

## References

- Profiling intake and collection checklist: `references/profiling-intake.md`
- Common code smells and remediation patterns: `references/code-smells.md`
- Audit output template: `references/report-template.md`
- Add Apple documentation and WWDC resources under `references/` as they are supplied by the user.
- Optimizing SwiftUI performance with Instruments: `references/optimizing-swiftui-performance-instruments.md`
- Understanding and improving SwiftUI performance: `references/understanding-improving-swiftui-performance.md`
- Understanding hangs in your app: `references/understanding-hangs-in-your-app.md`
- Demystify SwiftUI performance (WWDC23): `references/demystify-swiftui-performance-wwdc23.md`
