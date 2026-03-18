# Canonical Skill: skill-share

Generated at: `2026-03-18T09:12:23+00:00`
Translation status: `english`
Canonical ID: `skill--skill-share`

## Summary
A skill that creates new Claude skills and automatically shares them on Slack using Rube for seamless team collaboration and skill discovery.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `skill-share/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/skill-share/SKILL.md))

## Metadata
- Tags: `skill, skill-md, skill-share`
- Languages: `python`
- Systems: `slack`
- Jobs: `skill-md, skill-share`
- Roles: ``

## Steps
1. **Automatically share created skills** on Slack channels for team visibility
2. **Create new Claude skills** with proper structure and metadata
3. **Generate skill packages** ready for distribution
4. **Package and distribute** skills to your team
5. **User says he wants to create/share his skill**
6. **Validate skill structure** before sharing
7. Auto-generates YAML frontmatter with required metadata
8. Automating the skill development pipeline
9. Building internal tools that need skill creation + team notification
10. Checks naming conventions
11. Collaborative skill creation with team notifications
12. Creates distributable zip files
13. Creates properly structured skill directories with SKILL.md
14. Creating skills as part of team workflows
15. Enforces naming conventions (hyphen-case)
16. Ensures metadata completeness before packaging
17. Generates standardized scripts/, references/, and assets/ directories
18. Includes all skill assets and documentation
19. Runs validation automatically before packaging
20. Validates SKILL.md format and required fields

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: skill-share/SKILL.md
## When to use this skill

Use this skill when you need to:
- **Create new Claude skills** with proper structure and metadata
- **Generate skill packages** ready for distribution
- **Automatically share created skills** on Slack channels for team visibility
- **Validate skill structure** before sharing
- **Package and distribute** skills to your team

Also use this skill when:
- **User says he wants to create/share his skill** 

This skill is ideal for:
- Creating skills as part of team workflows
- Building internal tools that need skill creation + team notification
- Automating the skill development pipeline
- Collaborative skill creation with team notifications

## Key Features

### 1. Skill Creation
- Creates properly structured skill directories with SKILL.md
- Generates standardized scripts/, references/, and assets/ directories
- Auto-generates YAML frontmatter with required metadata
- Enforces naming conventions (hyphen-case)

### 2. Skill Validation
- Validates SKILL.md format and required fields
- Checks naming conventions
- Ensures metadata completeness before packaging

### 3. Skill Packaging
- Creates distributable zip files
- Includes all skill assets and documentation
- Runs validation automatically before packaging

### 4. Slack Integration via Rube
- Automatically sends created skill information to designated Slack channels
- Shares skill metadata (name, description, link)
- Posts skill summary for team discovery
- Provides direct links to skill files

## How It Works

1. **Initialization**: Provide skill name and description
2. **Creation**: Skill directory is created with proper structure
3. **Validation**: Skill metadata is validated for correctness
4. **Packaging**: Skill is packaged into a distributable format
5. **Slack Notification**: Skill details are posted to your team's Slack channel

## Example Usage

```
When you ask Claude to create a skill called "pdf-analyzer":
1. Creates /skill-pdf-analyzer/ with SKILL.md template
2. Generates structured directories (scripts/, references/, assets/)
3. Validates the skill structure
4. Packages the skill as a zip file
5. Posts to Slack: "New Skill Created: pdf-analyzer - Advanced PDF analysis and extraction capabilities"
```

## Integration with Rube

This skill leverages Rube for:
- **SLACK_SEND_MESSAGE**: Posts skill information to team channels
- **SLACK_POST_MESSAGE_WITH_BLOCKS**: Shares rich formatted skill metadata
- **SLACK_FIND_CHANNELS**: Discovers target channels for skill announcements

## Requirements

- Slack workspace connection via Rube
- Write access to skill creation directory
- Python 3.7+ for skill creation scripts
- Target Slack channel for skill notifications
