[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-2ea44f?logo=github)](https://dimillian.github.io/Skills/)

# Skills Public

A collection of reusable development skills for Apple platforms, GitHub workflows, React performance work, and skill curation.

## Overview

This repository contains focused, self-contained skills that help with recurring engineering tasks such as generating App Store release notes, debugging iOS apps, improving SwiftUI and React code, packaging macOS apps, and auditing what new skills a project actually needs.

Install: place these skill folders under `$CODEX_HOME/skills`


## Skills

This repo currently includes 11 skills:

| Skill | Folder | Description |
| --- | --- | --- |
| App Store Changelog | `app-store-changelog` | Creates user-facing App Store release notes from git history by collecting changes since the last tag, filtering for user-visible work, and rewriting it into concise "What's New" bullets. |
| GitHub | `github` | Uses the `gh` CLI to inspect and operate on GitHub issues, pull requests, workflow runs, and API data, including CI checks, run logs, and advanced queries. |
| iOS Debugger Agent | `ios-debugger-agent` | Uses XcodeBuildMCP to build, launch, and debug the current iOS app on a booted simulator, including UI inspection, interaction, screenshots, and log capture. |
| macOS SwiftPM App Packaging (No Xcode) | `macos-spm-app-packaging` | Scaffolds, builds, packages, signs, and optionally notarizes SwiftPM-based macOS apps without requiring an Xcode project. |
| Project Skill Audit | `project-skill-audit` | Analyzes a project's past Codex sessions, memory, existing local skills, and conventions to recommend the highest-value new skills or updates to existing ones. |
| React Component Performance | `react-component-performance` | Diagnoses slow React components by finding re-render churn, expensive render work, unstable props, and list bottlenecks, then suggests targeted optimizations and validation steps. |
| Swift Concurrency Expert | `swift-concurrency-expert` | Reviews and fixes Swift 6.2+ concurrency issues such as actor isolation problems, `Sendable` violations, main-actor annotations, and data-race diagnostics. |
| SwiftUI Liquid Glass | `swiftui-liquid-glass` | Implements, reviews, or refactors SwiftUI features to use the iOS 26+ Liquid Glass APIs correctly, with proper modifier ordering, grouping, interactivity, and fallbacks. |
| SwiftUI Performance Audit | `swiftui-performance-audit` | Audits SwiftUI runtime performance from code and architecture, focusing on invalidation storms, identity churn, layout thrash, heavy render work, and profiling guidance. |
| SwiftUI UI Patterns | `swiftui-ui-patterns` | Provides best practices and example-driven guidance for building SwiftUI screens and components, including navigation, sheets, app wiring, async state, and reusable UI patterns. |
| SwiftUI View Refactor | `swiftui-view-refactor` | Refactors SwiftUI view files toward smaller subviews, MV-style data flow, stable view trees, explicit dependency injection, and correct Observation usage. |

## Usage

Each skill is self-contained. Refer to the `SKILL.md` file in each skill directory for triggers, workflow guidance, examples, and supporting references.

## Contributing

Skills are designed to be focused and reusable. When adding new skills, ensure they:
- Have a clear, single purpose
- Include comprehensive documentation
- Follow consistent patterns with existing skills
- Include reference materials when applicable
