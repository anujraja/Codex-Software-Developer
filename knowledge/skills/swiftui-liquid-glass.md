# Canonical Skill: swiftui-liquid-glass

Generated at: `2026-03-18T08:03:51+00:00`
Translation status: `english`
Canonical ID: `skill--swiftui-liquid-glass`

## Summary
Implement, review, or improve SwiftUI features using the iOS 26+ Liquid Glass API. Use when asked to adopt Liquid Glass in new SwiftUI UI, refactor an existing feature to Liquid Glass, or review Liquid Glass usage for correctness, performance, and design alignment.

## Provenance
- `Dimillian/Skills` `main` `swiftui-liquid-glass/SKILL.md` ([raw](https://raw.githubusercontent.com/Dimillian/Skills/main/swiftui-liquid-glass/SKILL.md))

## Metadata
- Tags: `skill, skill-md, swiftui-liquid-glass`
- Languages: `swift`
- Systems: `docker, ios`
- Jobs: `skill-md, swiftui-liquid-glass`
- Roles: ``

## Steps
1. **Availability**: `#available(iOS 26, *)` present with fallback UI.
2. **Composition**: Multiple glass views wrapped in `GlassEffectContainer`.
3. **Interactivity**: `interactive()` only where user interaction exists.
4. **Modifier order**: `glassEffect` applied after layout/appearance modifiers.
5. **Transitions**: `glassEffectID` used with `@Namespace` for morphing.
6. Add glass modifiers after layout/appearance modifiers.
7. Add morphing transitions only when the view hierarchy changes with animation.
8. Apply `.glassEffect(...)` after layout and visual modifiers.
9. Check for iOS 26+ availability handling and sensible fallbacks.
10. Design the glass surfaces and interactions first (shape, prominence, grouping).
11. Gate with `#available(iOS 26, *)` and provide a non-glass fallback.
12. Identify target components for glass treatment (surfaces, chips, buttons, cards).
13. Inspect where Liquid Glass should be used and where it should not.
14. Introduce interactive glass only for tappable or focusable elements.
15. Keep shapes consistent across related elements for a cohesive look.
16. Prefer native Liquid Glass APIs over custom blurs.
17. Refactor to use `GlassEffectContainer` where multiple glass elements appear.
18. Use `.interactive()` for elements that respond to touch/pointer.
19. Use `GlassEffectContainer` when multiple glass elements coexist.
20. Verify correct modifier order, shape usage, and container placement.

## Instructions
Source: Dimillian/Skills (main) :: swiftui-liquid-glass/SKILL.md
# SwiftUI Liquid Glass

## Overview
Use this skill to build or review SwiftUI features that fully align with the iOS 26+ Liquid Glass API. Prioritize native APIs (`glassEffect`, `GlassEffectContainer`, glass button styles) and Apple design guidance. Keep usage consistent, interactive where needed, and performance aware.

## Workflow Decision Tree
Choose the path that matches the request:

### 1) Review an existing feature
- Inspect where Liquid Glass should be used and where it should not.
- Verify correct modifier order, shape usage, and container placement.
- Check for iOS 26+ availability handling and sensible fallbacks.

### 2) Improve a feature using Liquid Glass
- Identify target components for glass treatment (surfaces, chips, buttons, cards).
- Refactor to use `GlassEffectContainer` where multiple glass elements appear.
- Introduce interactive glass only for tappable or focusable elements.

### 3) Implement a new feature using Liquid Glass
- Design the glass surfaces and interactions first (shape, prominence, grouping).
- Add glass modifiers after layout/appearance modifiers.
- Add morphing transitions only when the view hierarchy changes with animation.

## Core Guidelines
- Prefer native Liquid Glass APIs over custom blurs.
- Use `GlassEffectContainer` when multiple glass elements coexist.
- Apply `.glassEffect(...)` after layout and visual modifiers.
- Use `.interactive()` for elements that respond to touch/pointer.
- Keep shapes consistent across related elements for a cohesive look.
- Gate with `#available(iOS 26, *)` and provide a non-glass fallback.

## Review Checklist
- **Availability**: `#available(iOS 26, *)` present with fallback UI.
- **Composition**: Multiple glass views wrapped in `GlassEffectContainer`.
- **Modifier order**: `glassEffect` applied after layout/appearance modifiers.
- **Interactivity**: `interactive()` only where user interaction exists.
- **Transitions**: `glassEffectID` used with `@Namespace` for morphing.
- **Consistency**: Shapes, tinting, and spacing align across the feature.

## Implementation Checklist
- Define target elements and desired glass prominence.
- Wrap grouped glass elements in `GlassEffectContainer` and tune spacing.
- Use `.glassEffect(.regular.tint(...).interactive(), in: .rect(cornerRadius: ...))` as needed.
- Use `.buttonStyle(.glass)` / `.buttonStyle(.glassProminent)` for actions.
- Add morphing transitions with `glassEffectID` when hierarchy changes.
- Provide fallback materials and visuals for earlier iOS versions.

## Quick Snippets
Use these patterns directly and tailor shapes/tints/spacing.

```swift
if #available(iOS 26, *) {
    Text("Hello")
        .padding()
        .glassEffect(.regular.interactive(), in: .rect(cornerRadius: 16))
} else {
    Text("Hello")
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}
```

```swift
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        Image(systemName: "scribble.variable")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
        Image(systemName: "eraser.fill")
            .frame(width: 72, height: 72)
            .font(.system(size: 32))
            .glassEffect()
    }
}
```

```swift
Button("Confirm") { }
    .buttonStyle(.glassProminent)
```

## Resources
- Reference guide: `references/liquid-glass.md`
- Prefer Apple docs for up-to-date API details.
