# Canonical Skill: brand-guidelines

Generated at: `2026-03-18T19:24:23+00:00`
Translation status: `english`
Canonical ID: `skill--brand-guidelines`

## Summary
Applies OpenAI's brand colors and typography to any artifact that should match the Codex/OpenAI look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.

## Provenance
- `ComposioHQ/awesome-codex-skills` `master` `brand-guidelines/SKILL.md` ([raw](https://raw.githubusercontent.com/ComposioHQ/awesome-codex-skills/master/brand-guidelines/SKILL.md))

## Metadata
- Tags: `brand-guidelines, skill, skill-md`
- Languages: ``
- Systems: `azure`
- Jobs: `brand-guidelines, skill-md`
- Roles: ``

## Steps
1. **Body Text**: Inter, Regular (with Arial fallback)
2. **Code/Monospace**: IBM Plex Mono (with Menlo/monospace fallback)
3. **Headings**: Inter, Semibold/Bold (with Arial fallback)
4. **Note**: Fonts should be pre-installed in your environment for best results
5. Applies IBM Plex Mono for code snippets or inline code
6. Applies Inter Regular to body text
7. Applies Inter Semibold/Bold to headings (24pt and larger)
8. Automatically falls back to Arial/Menlo if custom fonts unavailable
9. Azure: `#2B8FFF` - Secondary accent
10. Body text: Inter Regular
11. Charcoal: `#0E0F12` - Primary text and dark backgrounds
12. Graphite: `#40434A` - Neutral accent for icons or strokes
13. Headings (24pt+): Inter Semibold/Bold
14. Mist: `#F5F7FA` - Light backgrounds and text on dark
15. OpenAI Green: `#10A37F` - Primary accent
16. Preserves readability across all systems
17. Preserves text hierarchy and formatting
18. Slate: `#202123` - Surface backgrounds
19. Smart color selection based on background (Charcoal or Mist as appropriate)
20. Steel: `#9EA1AA` - Secondary elements and dividers

## Instructions
Source: ComposioHQ/awesome-codex-skills (master) :: brand-guidelines/SKILL.md
# OpenAI Brand Styling

## Overview

Apply OpenAI's brand identity and style resources with this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, OpenAI brand, Codex, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- Charcoal: `#0E0F12` - Primary text and dark backgrounds
- Slate: `#202123` - Surface backgrounds
- Mist: `#F5F7FA` - Light backgrounds and text on dark
- Steel: `#9EA1AA` - Secondary elements and dividers

**Accent Colors:**

- OpenAI Green: `#10A37F` - Primary accent
- Azure: `#2B8FFF` - Secondary accent
- Graphite: `#40434A` - Neutral accent for icons or strokes

### Typography

- **Headings**: Inter, Semibold/Bold (with Arial fallback)
- **Body Text**: Inter, Regular (with Arial fallback)
- **Code/Monospace**: IBM Plex Mono (with Menlo/monospace fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Inter Semibold/Bold to headings (24pt and larger)
- Applies Inter Regular to body text
- Applies IBM Plex Mono for code snippets or inline code
- Automatically falls back to Arial/Menlo if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Inter Semibold/Bold
- Body text: Inter Regular
- Smart color selection based on background (Charcoal or Mist as appropriate)
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycle accent usage: OpenAI Green → Azure → Graphite
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Inter and IBM Plex Mono fonts when available
- Provides automatic fallback to Arial (headings/body) and Menlo/monospace (code)
- No font installation required - works with existing system fonts
- For best results, pre-install Inter and IBM Plex Mono fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems
