---
name: modern-ui-ux-theming
description: Implement modern UI/UX design with theming, design systems, color theory, typography, and spacing. Use when creating design systems, implementing themes, choosing color palettes, setting up design tokens, or building consistent user experiences across applications.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
author: Claude Code
tags: [ui, ux, design, theming, design-system, colors, typography, spacing, tokens, accessibility, modern-design]
---

# Modern UI/UX Theming & Design Systems

Create beautiful, accessible, and consistent user experiences using modern design principles, theming systems, and design tokens. Build scalable design systems that work across platforms and frameworks.

## Overview

Modern UI/UX theming combines design principles, design tokens, and systematic approaches to create cohesive user experiences. This skill covers color theory, typography, spacing, design tokens, accessibility, and implementation strategies for modern applications.

## When to Use This Skill

**Activate when:**
- Creating a design system from scratch
- Implementing theming in applications
- Choosing color palettes and typography
- Setting up design tokens
- Ensuring accessibility compliance
- Building consistent UI across platforms
- Migrating to modern design principles

**Trigger keywords:** "design system", "theming", "color palette", "typography", "design tokens", "ui/ux", "accessibility", "spacing system"

**NOT for:**
- Quick prototypes without design requirements
- Applications not needing visual consistency
- Backend-only projects

## Prerequisites

**Required:**
- Basic understanding of CSS
- Knowledge of design fundamentals
- Project using modern framework (Next.js, React, etc.)

**Recommended:**
- Tailwind CSS or CSS-in-JS
- Design tool familiarity (Figma, etc.)
- Accessibility awareness (WCAG guidelines)

## Instructions

### Phase 1: Design System Foundation

#### Step 1: Define Design Principles

**Establish core principles:**
- Consistency - Uniform patterns
- Clarity - Clear communication
- Simplicity - Minimal complexity
- Accessibility - Inclusive design
- Scalability - Growth-ready

**See:** `references/design-principles.md`

#### Step 2: Create Color System

**Implement 60-30-10 rule:**
- 60% - Primary/dominant color
- 30% - Secondary color
- 10% - Accent color

**Define color scales:**
```css
/* Primary scale (50-950) */
--primary-50: oklch(0.98 0.01 240);
--primary-500: oklch(0.55 0.22 240);
--primary-950: oklch(0.20 0.08 240);
```

**See:** `references/color-systems.md`

#### Step 3: Establish Typography Scale

**Define type scale:**
- Font families (heading, body, mono)
- Size scale (xs, sm, base, lg, xl, 2xl, etc.)
- Line heights (tight, normal, relaxed)
- Font weights (normal, medium, semibold, bold)

**Example:**
```css
--font-sans: system-ui, sans-serif;
--text-xs: 0.75rem;
--text-base: 1rem;
--text-2xl: 1.5rem;
```

**See:** `references/typography-guide.md`

#### Step 4: Create Spacing System

**Use consistent scale:**
- Base unit (4px or 8px)
- Spacing scale (0, 1, 2, 4, 8, 12, 16, 24, 32, 48, 64)
- Apply to margins, padding, gaps

**Example:**
```css
--spacing-1: 0.25rem; /* 4px */
--spacing-4: 1rem;    /* 16px */
--spacing-8: 2rem;    /* 32px */
```

**See:** `references/spacing-guide.md`

### Phase 2: Design Tokens

#### Step 5: Set Up Design Tokens

**Create token structure:**
```json
{
  "color": {
    "primary": { "value": "#3b82f6" },
    "surface": { "value": "#ffffff" }
  },
  "spacing": {
    "small": { "value": "0.5rem" },
    "medium": { "value": "1rem" }
  }
}
```

**See:** `references/design-tokens.md`

#### Step 6: Implement Semantic Tokens

**Map to meaning:**
```css
/* Semantic tokens */
--color-text-primary: var(--gray-900);
--color-text-secondary: var(--gray-600);
--color-bg-primary: var(--white);
--color-border-default: var(--gray-200);
```

**See:** `references/semantic-tokens.md`

### Phase 3: Theming Implementation

#### Step 7: Create Theme Structure

**Define themes:**
```css
/* Light theme */
[data-theme="light"] {
  --background: oklch(1 0 0);
  --foreground: oklch(0.1 0 0);
}

/* Dark theme */
[data-theme="dark"] {
  --background: oklch(0.1 0 0);
  --foreground: oklch(0.98 0 0);
}
```

**See:** `references/theme-implementation.md`

#### Step 8: Implement Theme Switching

**Quick:**
```typescript
// Use CSS variables + class/attribute toggle
document.documentElement.setAttribute('data-theme', 'dark')
```

**See:** `references/examples.md#theme-switching`

### Phase 4: Component Styling

#### Step 9: Apply Design System to Components

**Use tokens consistently:**
```css
.button {
  padding: var(--spacing-2) var(--spacing-4);
  background: var(--color-primary);
  color: var(--color-primary-foreground);
  border-radius: var(--radius-md);
}
```

**See:** `references/component-patterns.md`

#### Step 10: Create Variant System

**Define variants:**
```typescript
const buttonVariants = {
  variant: {
    primary: "bg-primary text-primary-foreground",
    secondary: "bg-secondary text-secondary-foreground",
    outline: "border border-input bg-background"
  },
  size: {
    sm: "h-9 px-3",
    md: "h-10 px-4",
    lg: "h-11 px-8"
  }
}
```

**See:** `references/variant-systems.md`

### Phase 5: Accessibility

#### Step 11: Ensure Color Contrast

**Check WCAG compliance:**
- AA: 4.5:1 for normal text
- AA: 3:1 for large text
- AAA: 7:1 for normal text

**Test tools:**
- Browser DevTools
- Contrast checkers

**See:** `references/accessibility-guide.md`

#### Step 12: Implement Focus States

**Visible focus indicators:**
```css
:focus-visible {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}
```

**See:** `references/accessibility-guide.md#focus-states`

### Phase 6: Responsive Design

#### Step 13: Create Breakpoint System

**Define breakpoints:**
```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
```

**See:** `references/responsive-design.md`

#### Step 14: Implement Fluid Typography

**Use clamp() for scaling:**
```css
font-size: clamp(1rem, 2vw + 0.5rem, 1.5rem);
```

**See:** `references/typography-guide.md#fluid`

### Phase 7: Documentation

#### Step 15: Document Design System

**Create documentation:**
- Color palette with use cases
- Typography specimens
- Component library
- Usage guidelines
- Code examples

**See:** `references/documentation-template.md`

#### Step 16: Create Style Guide

**Include:**
- Brand guidelines
- Component dos and don'ts
- Accessibility requirements
- Code standards

**See:** `references/style-guide-template.md`

## Common Patterns

### Pattern 1: Minimalist Design
**Principles:** Clean, uncluttered, focus on essentials, generous whitespace

**See:** `references/design-patterns.md#minimalist`

### Pattern 2: Dark Mode
**Quick:** CSS variables + theme toggle + proper contrast

**See:** `references/examples.md#dark-mode`

### Pattern 3: Design Tokens
**Quick:** JSON/CSS variables → build tools → platform outputs

**See:** `references/design-tokens.md`

### Pattern 4: Component Theming
**Quick:** Base styles + variant system + token integration

**See:** `references/component-patterns.md`

### Pattern 5: Accessible Color System
**Quick:** Generate scales → test contrast → document usage

**See:** `references/color-systems.md#accessible`

## Quick Reference

**Design Principles:** Consistency, Clarity, Simplicity, Accessibility
**Color Theory:** 60-30-10 rule, semantic colors
**Typography:** Font hierarchy, readability (50-75 chars, 1.5-1.75 line height)
**Spacing:** 4px/8px base, geometric scale

**See:** `references/design-principles.md`, `references/color-systems.md`, `references/typography-guide.md`, `references/spacing-guide.md`

## Error Handling

| Issue | Cause | Solution |
|-------|-------|----------|
| Poor contrast | Colors too similar | Adjust lightness values |
| Inconsistent spacing | No spacing system | Implement token-based spacing |
| Typography hierarchy unclear | Similar sizes | Increase scale contrast |
| Theme not switching | CSS vars not updating | Check theme provider setup |
| Accessibility fails | Missing focus states | Add visible focus indicators |

**See:** `references/troubleshooting.md`

## Integration with Other Skills

### With styling-with-shadcn
Apply design tokens to shadcn components:
- Override CSS variables
- Customize component variants
- Implement custom themes

### With better-auth-nextjs
Design auth UI with system:
- Consistent form styling
- Brand-aligned colors
- Accessible interactions

### With nextjs-dev-tool
Test design implementation:
- Browser automation for themes
- Visual regression testing
- Accessibility checks

**See:** `references/integration-guides.md`

## Best Practices

1. **Start with tokens** - Define before implementing
2. **Test accessibility** - Check contrast and focus states
3. **Document everything** - Clear guidelines prevent inconsistency
4. **Use semantic naming** - `--color-text-primary` not `--color-gray-900`
5. **Mobile first** - Design for smallest screens
6. **Performance matters** - Optimize assets and animations
7. **Test with users** - Real feedback trumps assumptions
8. **Version your system** - Track changes systematically

## Validation Checklist

**Design System:**
- [ ] Color palette defined with scales
- [ ] Typography system established
- [ ] Spacing scale implemented
- [ ] Design tokens created
- [ ] Semantic tokens mapped

**Implementation:**
- [ ] Themes switch correctly
- [ ] Components use tokens
- [ ] Responsive breakpoints work
- [ ] Accessibility standards met
- [ ] Documentation complete

**Quality:**
- [ ] WCAG AA contrast ratios
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Cross-browser tested
- [ ] Performance optimized

## Tools and Resources

**Color Tools:**
- Oklch Color Picker
- Contrast Checkers
- Palette Generators

**Typography:**
- Modular Scale Calculator
- Font Pairing Tools
- Type Testers

**Design Tokens:**
- Style Dictionary
- Theo
- Design Tokens Community

**Accessibility:**
- axe DevTools
- WAVE
- Lighthouse

**See:** `references/tools-and-resources.md`

## References

**Local Documentation:**
- Design principles: `references/design-principles.md`
- Color systems: `references/color-systems.md`
- Typography guide: `references/typography-guide.md`
- Spacing guide: `references/spacing-guide.md`
- Design tokens: `references/design-tokens.md`
- Semantic tokens: `references/semantic-tokens.md`
- Theme implementation: `references/theme-implementation.md`
- Component patterns: `references/component-patterns.md`
- Accessibility guide: `references/accessibility-guide.md`
- Examples: `references/examples.md`
- Integration guides: `references/integration-guides.md`
- Troubleshooting: `references/troubleshooting.md`

**External Resources:**
- [Modern UI/UX Design Principles 2025](https://cms.emergen.io/2025/10/30/modern-ui-ux-design-principles-best-practices-for-2025-a-complete-guide/)
- [Top Design System Guides](https://uidesignz.com/blogs/top-design-system-guides)
- [Typography & Color Principles](https://www.elinext.com/services/ui-ux-design/trends/typography-color-principles-in-ui-ux-design/)
- [UI Design Principles 2026](https://www.lyssna.com/blog/ui-design-principles/)
- [Carbon Design System](https://carbondesignsystem.com)
- [Lightning Design System](https://www.lightningdesignsystem.com)

## Tips for Success

1. **Start simple** - Build complexity gradually
2. **Be consistent** - Use tokens everywhere
3. **Test early** - Accessibility from day one
4. **Document as you go** - Don't wait until the end
5. **Get feedback** - Test with real users
6. **Iterate** - Design systems evolve
7. **Automate** - Use tools for token generation
8. **Stay current** - Modern design principles evolve

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Design system foundation
- Color theory and palettes
- Typography systems
- Spacing and layout
- Design tokens
- Theming implementation
- Accessibility guidelines
- Component patterns
- Integration guides

## Sources

- [Modern UI/UX Design Principles 2025](https://cms.emergen.io/2025/10/30/modern-ui-ux-design-principles-best-practices-for-2025-a-complete-guide/)
- [Top Design System Guides](https://uidesignz.com/blogs/top-design-system-guides)
- [Typography & Color Principles](https://www.elinext.com/services/ui-ux-design/trends/typography-color-principles-in-ui-ux-design/)
- [UI Design Principles 2026](https://www.lyssna.com/blog/ui-design-principles/)
- [User Interface Design Principles 2024](https://medium.com/@uidesign0005/top-10-user-interface-design-principles-in-2024-e18702a5d395)
