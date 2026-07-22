---
name: landing-page-design-2026
description: Design and implement modern 2026-style landing pages with anticipatory UX, kinetic typography, scrollytelling, and eco-conscious themes. Provides Tailwind configurations, framer-motion micro-interactions, and design-system templates.
version: 1.0.0
allowed-tools: Bash, Read, Write, Glob, Grep
author: Claude Code
tags: [ui, ux, design, landing-page, tailwind, framer-motion]
---

# Landing Page Design 2026

## Overview
Implement cutting-edge landing pages based on 2025-2026 design trends. Focuses on **Anticipatory Design**, **Kinetic Typography**, **Strategic Maximalism**, and **Eco-conscious Dark Themes**.

## When to Use This Skill
- Building high-conversion landing pages
- Transitioning to modern "app-like" mobile-first web experiences
- Implementing narrative-driven storytelling (scrollytelling)
- Setting up modern color palettes and micro-interactions

## Prerequisites
- Next.js (App Router preferred)
- Tailwind CSS
- Framer Motion (recommended for micro-interactions)
- Lucide React (for icons)

## Instructions

### Phase 1: Design System Setup
1. Define the **Eco-conscious Dark Theme** in `tailwind.config.ts`.
2. Configure **Hero Typography** (Variable fonts with tight tracking).
3. **See:** `references/quick-reference.md#tailwind-config`

### Phase 2: Hero & Typography
1. Implement **Kinetic Typography** for the Hero section.
2. Use large, bold fonts where text *is* the primary visual element.
3. **See:** `references/examples.md#hero-typography-component`

### Phase 3: Scrollytelling & UX
1. Build section transitions using scroll-triggered animations.
2. Implement **Anticipatory Design** triggers (personalized CTAs based on data).
3. **See:** `references/examples.md#scrollytelling-section`

### Phase 4: Micro-interactions
1. Add functional feedback to buttons and forms.
2. Implement custom cursor interactions (flashlight/scale effects).
3. **See:** `references/examples.md#micro-interactions-snippets`

## Common Patterns
- **The "Flashlight" Dark Mode**: User cursor reveals content in a dark, textured grid.
- **Narrative Scroll**: Reveal problem -> solution -> social proof with smooth transitions.
- **Anticipatory CTA**: Update button text based on user's referring source.

## Error Handling
| Issue | Solution |
|-------|----------|
| Animation Lag | Reduce `framer-motion` layout animations; use `will-change`. |
| Font Flash (FOIT) | Use WOFF2 and `font-display: swap`. |
| Contrast Accessibility | Check eco-conscious palettes against WCAG 2.1 (APCA preferred). |

## References
- Examples: `references/examples.md`
- Quick Reference: `references/quick-reference.md`
- Modern Trends: `references/trends-2026.md`
- Troubleshooting: `references/troubleshooting.md`
