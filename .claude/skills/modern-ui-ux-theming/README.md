# Modern UI/UX Theming & Design Systems

A comprehensive Claude Code skill for implementing modern design principles, theming systems, and design tokens to create beautiful, accessible, and consistent user experiences.

## Overview

This skill provides guidance on creating scalable design systems using modern principles including color theory, typography, spacing, design tokens, and accessibility. Build cohesive experiences that work across platforms and frameworks.

## Features

### ✅ Design System Foundation
- Core design principles
- Color theory and palettes
- Typography systems
- Spacing and layout principles
- Design token architecture

### ✅ Theming Implementation
- Light/dark mode support
- CSS variables and tokens
- Theme switching logic
- Semantic token mapping
- Cross-framework compatibility

### ✅ Accessibility
- WCAG 2.1 compliance guidelines
- Color contrast testing
- Focus state management
- Keyboard navigation
- Screen reader compatibility

### ✅ Modern Design Principles
- Minimalism and clarity
- Consistent visual hierarchy
- Responsive design patterns
- Performance optimization
- User feedback patterns

## Installation

```bash
# Copy to project skills
cp -r modern-ui-ux-theming /path/to/project/.claude/skills/

# Or copy to global skills
cp -r modern-ui-ux-theming ~/.claude/skills/
```

## Usage

### Activation

The skill activates with trigger keywords:
- "design system"
- "theming"
- "color palette"
- "typography"
- "design tokens"
- "ui/ux"
- "accessibility"
- "spacing system"

### Example Prompts

**Design System Creation:**
- "Create a design system for my app"
- "Set up design tokens with color scales"
- "Implement a typography system"

**Theming:**
- "Add dark mode to my application"
- "Create theme switching functionality"
- "Set up CSS variables for theming"

**Color & Typography:**
- "Choose an accessible color palette"
- "Set up a type scale"
- "Implement the 60-30-10 color rule"

**Accessibility:**
- "Check color contrast ratios"
- "Add focus states to components"
- "Ensure WCAG AA compliance"

## Documentation Structure

```
modern-ui-ux-theming/
├── SKILL.md (470 lines)              # Main workflow
├── README.md                          # This file
├── references/
│   ├── design-principles.md           # Core principles
│   ├── color-systems.md               # Color theory
│   ├── typography-guide.md            # Typography systems
│   ├── spacing-guide.md               # Spacing principles
│   ├── design-tokens.md               # Token architecture
│   ├── semantic-tokens.md             # Semantic mapping
│   ├── theme-implementation.md        # Theming guide
│   ├── component-patterns.md          # Component styling
│   ├── accessibility-guide.md         # WCAG compliance
│   ├── examples.md                    # Complete examples
│   └── integration-guides.md          # Skill integration
├── assets/
│   └── templates/
│       ├── design-tokens.json         # Token template
│       ├── theme-config.css           # Theme template
│       └── component-variants.ts      # Variant template
└── scripts/
    └── generate-tokens.sh             # Token generator
```

## Key Concepts

### Design Principles

**Consistency** - Uniform patterns across all UI elements
**Clarity** - Clear visual hierarchy and communication
**Simplicity** - Minimal cognitive load for users
**Accessibility** - Inclusive design for all users
**Scalability** - System grows with application

### Color Theory

**60-30-10 Rule:**
- 60% Dominant color (primary)
- 30% Secondary color
- 10% Accent color

**Color Scales:** 50-950 for each color with proper contrast

### Typography

**Hierarchy:** Size, weight, and color create clear information structure
**Readability:** 50-75 character line length, 1.5-1.75 line height
**Font Selection:** Sans-serif for UI, serif for content, monospace for code

### Spacing System

**Base Unit:** 4px or 8px
**Scale:** Geometric progression (4, 8, 12, 16, 24, 32, 48, 64)
**Application:** Consistent margins, padding, and gaps

### Design Tokens

**Foundation Tokens:** Base values (colors, sizes)
**Semantic Tokens:** Purpose-based (`--color-text-primary`)
**Component Tokens:** Component-specific values

## Common Use Cases

### Creating a Brand Design System
Define colors, typography, spacing that align with brand identity

### Implementing Dark Mode
Set up theme switching with proper contrast and accessibility

### Building Component Library
Style components using design tokens for consistency

### Ensuring Accessibility
Test and implement WCAG compliance throughout design

### Multi-Platform Consistency
Design tokens that work across web, mobile, desktop

## Integration with Other Skills

### With styling-with-shadcn
- Apply design tokens to shadcn components
- Override theme variables
- Implement custom color scales

### With better-auth-nextjs
- Design auth UI with consistent theming
- Apply accessible color contrast
- Style forms with design system

### With nextjs-dev-tool
- Test theme switching
- Verify accessibility
- Check responsive breakpoints

See `references/integration-guides.md` for detailed workflows.

## Best Practices

1. **Start with tokens** - Define design tokens before implementation
2. **Test accessibility** - Check contrast ratios and focus states early
3. **Document thoroughly** - Clear guidelines prevent inconsistency
4. **Use semantic naming** - `--text-primary` not `--gray-900`
5. **Mobile first** - Design for smallest screens first
6. **Test with real users** - Get feedback early and often
7. **Version your system** - Track changes systematically
8. **Automate testing** - Use tools for contrast and accessibility checks

## Tools Covered

**Color:**
- Oklch Color Picker
- Contrast Checkers
- Palette Generators

**Typography:**
- Modular Scale Calculators
- Font Pairing Tools

**Design Tokens:**
- Style Dictionary
- Theo

**Accessibility:**
- axe DevTools
- WAVE
- Lighthouse

## Accessibility Standards

**WCAG 2.1 Levels:**
- **Level A:** Basic accessibility
- **Level AA:** Standard compliance (recommended)
- **Level AAA:** Enhanced accessibility

**Contrast Ratios:**
- Normal text: 4.5:1 (AA), 7:1 (AAA)
- Large text: 3:1 (AA), 4.5:1 (AAA)
- UI components: 3:1

## Requirements

**Knowledge:**
- Basic CSS understanding
- Design fundamentals
- Framework basics (Next.js, React, etc.)

**Tools:**
- Modern code editor
- Browser DevTools
- Design tool (optional: Figma, Sketch)

## Resources

**Official Documentation:**
- [Modern UI/UX Design Principles 2025](https://cms.emergen.io/2025/10/30/modern-ui-ux-design-principles-best-practices-for-2025-a-complete-guide/)
- [Top Design System Guides](https://uidesignz.com/blogs/top-design-system-guides)
- [Typography & Color Principles](https://www.elinext.com/services/ui-ux-design/trends/typography-color-principles-in-ui-ux-design/)
- [UI Design Principles 2026](https://www.lyssna.com/blog/ui-design-principles/)

**Design Systems:**
- [Carbon Design System (IBM)](https://carbondesignsystem.com)
- [Lightning Design System (Salesforce)](https://www.lightningdesignsystem.com)
- [Material Design (Google)](https://m3.material.io)

**Local Documentation:**
- Complete principles: `references/design-principles.md`
- Color guide: `references/color-systems.md`
- Typography: `references/typography-guide.md`
- Examples: `references/examples.md`

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Design system foundation
- Color theory and implementation
- Typography systems
- Spacing and layout
- Design tokens architecture
- Theming with light/dark modes
- Accessibility guidelines (WCAG 2.1)
- Component styling patterns
- Integration with existing skills
- Progressive disclosure structure (470 lines)

## Support

- Design Systems Community
- [A11y Project](https://www.a11yproject.com)
- [Web Content Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## Contributing

Improvements welcome! Please ensure:
- SKILL.md stays under 500 lines
- Examples follow modern best practices
- Accessibility guidelines are accurate
- Integration guides are updated

---

**Created with:** Claude Code + skill-creator + web research + Context7 MCP
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
