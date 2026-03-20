# Canonical Skill: changelog-generator

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--changelog-generator`

## Summary
Automatically creates user-facing changelogs from git commits by analyzing commit history, categorizing changes, and transforming technical commits into clear, customer-friendly release notes. Turns hours of manual changelog writing into minutes of automated generation.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `changelog-generator/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/changelog-generator/SKILL.md))

## Metadata
- Tags: `changelog-generator, skill, skill-md`
- Languages: ``
- Systems: `git, github`
- Jobs: `changelog-generator, skill-md`
- Roles: `developer`

## Steps
1. **Better Search**: Search now includes file contents, not just titles
2. **Categorizes Changes**: Groups commits into logical categories (features, improvements, bug fixes, breaking changes, security)
3. **Faster Sync**: Files now sync 2x faster across devices
4. **Filters Noise**: Excludes internal commits (refactoring, tests, etc.)
5. **Follows Best Practices**: Applies changelog guidelines and your brand voice
6. **Formats Professionally**: Creates clean, structured changelog entries
7. **Keyboard Shortcuts**: Press ? to see all available shortcuts.
8. **Scans Git History**: Analyzes commits from a specific time period or between versions
9. **Team Workspaces**: Create separate workspaces for different
10. **Translates Technical → User-Friendly**: Converts developer commits into customer language
11. Corrected notification badge count
12. Creating internal release documentation
13. Creating weekly or monthly product update summaries
14. Documenting changes for customers
15. Fixed issue where large images wouldn't upload
16. Generating update notifications
17. Maintaining a public changelog/product updates page
18. Preparing release notes for a new version
19. Resolved timezone confusion in scheduled posts
20. Writing changelog entries for app store submissions

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: changelog-generator/SKILL.md
# Changelog Generator

This skill transforms technical git commits into polished, user-friendly changelogs that your customers and users will actually understand and appreciate.

## When to Use This Skill

- Preparing release notes for a new version
- Creating weekly or monthly product update summaries
- Documenting changes for customers
- Writing changelog entries for app store submissions
- Generating update notifications
- Creating internal release documentation
- Maintaining a public changelog/product updates page

## What This Skill Does

1. **Scans Git History**: Analyzes commits from a specific time period or between versions
2. **Categorizes Changes**: Groups commits into logical categories (features, improvements, bug fixes, breaking changes, security)
3. **Translates Technical → User-Friendly**: Converts developer commits into customer language
4. **Formats Professionally**: Creates clean, structured changelog entries
5. **Filters Noise**: Excludes internal commits (refactoring, tests, etc.)
6. **Follows Best Practices**: Applies changelog guidelines and your brand voice

## How to Use

### Basic Usage

From your project repository:

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### With Specific Date Range

```
Create a changelog for all commits between March 1 and March 15
```

### With Custom Guidelines

```
Create a changelog for commits since v2.4.0, using my changelog 
guidelines from CHANGELOG_STYLE.md
```

## Example

**User**: "Create a changelog for commits from the past 7 days"

**Output**:
```markdown
# Updates - Week of March 10, 2024

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different 
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts. 
  Navigate faster without touching your mouse.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## 🐛 Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count
```

**Inspired by:** Manik Aggarwal's use case from Lenny's Newsletter

## Tips

- Run from your git repository root
- Specify date ranges for focused changelogs
- Use your CHANGELOG_STYLE.md for consistent formatting
- Review and adjust the generated changelog before publishing
- Save output directly to CHANGELOG.md

## Related Use Cases

- Creating GitHub release notes
- Writing app store update descriptions
- Generating email updates for users
- Creating social media announcement posts
