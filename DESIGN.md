---
version: alpha
name: "Shovels Intelligence Layer"
description: "Shovels is an AI-powered construction permit intelligence platform. The design uses a single custom typeface (Scandia via Adobe Fonts) across all type roles, anchored by a deep forest-green brand palette (#01654d / #065f46) against near-black text (#101727 / #111827) on white and light-lime tinted surfaces (#f7fee7). The layout is a standard marketing hero with a wide max-width container, generous section spacing, and a clear CTA hierarchy. Radius language mixes full-pill badges with 6–16px rounded rectangles. Elevation is minimal. only subtle 1px inset ring shadows and a single 1px drop shadow on form inputs."
colors:
  border-gray: "#e5e7eb"
  lime-tint-surface: "#f7fee7"
  page-white: "#ffffff"
  amber-accent: "#e9be51"
  dark-forest-green: "#065f46"
  deep-navy-text: "#101727"
  forest-green-primary: "#01654d"
  light-amber: "#fcd34d"
  mid-gray-text: "#4b5563"
  muted-gray: "#9ca3af"
  near-black-heading: "#111827"
  light-border-gray: "#d1d5db"
typography:
  hero-display:
    fontFamily: "Scandia"
    fontSize: "72px"
    fontWeight: "600"
    lineHeight: "72px"
    letterSpacing: "-1.8px"
  section-heading:
    fontFamily: "Scandia"
    fontSize: "48px"
    fontWeight: "600"
    lineHeight: "48px"
    letterSpacing: "-1.2px"
  sub-heading:
    fontFamily: "Scandia"
    fontSize: "30px"
    fontWeight: "600"
    lineHeight: "36px"
    letterSpacing: "-0.75px"
  card-heading:
    fontFamily: "Scandia"
    fontSize: "20px"
    fontWeight: "500"
    lineHeight: "32px"
  body-large:
    fontFamily: "Scandia"
    fontSize: "18px"
    fontWeight: "400"
    lineHeight: "32px"
  body-default:
    fontFamily: "Scandia"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "24px"
  body-relaxed:
    fontFamily: "Scandia"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "28px"
  body-medium:
    fontFamily: "Scandia"
    fontSize: "16px"
    fontWeight: "500"
    lineHeight: "24px"
  label-semibold:
    fontFamily: "Scandia"
    fontSize: "16px"
    fontWeight: "600"
    lineHeight: "16px"
  small-default:
    fontFamily: "Scandia"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "24px"
  small-semibold:
    fontFamily: "Scandia"
    fontSize: "14px"
    fontWeight: "600"
    lineHeight: "24px"
  caption:
    fontFamily: "Scandia"
    fontSize: "12px"
    fontWeight: "400"
    lineHeight: "16px"
rounded:
  radius-sm: "6px"
  radius-md: "8px"
  radius-lg: "16px"
  radius-full: "9999px"
spacing:
  spacing-2: "8px"
  spacing-3: "12px"
  spacing-4: "16px"
  spacing-5: "20px"
  spacing-6: "24px"
  spacing-8: "32px"
  spacing-9: "36px"
  spacing-10: "40px"
  spacing-16: "64px"
  spacing-24: "96px"
  spacing-32: "128px"
---

## Overview

Shovels is an AI-powered construction permit intelligence platform. The design uses a single custom typeface (Scandia via Adobe Fonts) across all type roles, anchored by a deep forest-green brand palette (#01654d / #065f46) against near-black text (#101727 / #111827) on white and light-lime tinted surfaces (#f7fee7). The layout is a standard marketing hero with a wide max-width container, generous section spacing, and a clear CTA hierarchy. Radius language mixes full-pill badges with 6–16px rounded rectangles. Elevation is minimal. only subtle 1px inset ring shadows and a single 1px drop shadow on form inputs.

**Signature traits:**
- Single-family weight hierarchy: Builds hierarchy from Scandia across 3 weights rather than multiple families.
- Soft, rounded geometry: Generous corner rounding up to 9999px.
- Layered elevation: Depth comes from 3 validated shadow tokens.

## Colors

The palette uses 12 validated color tokens across 1 theme profile. Semantic roles stay attached to observed usage so generation agents can choose accents without inventing new color meaning.

**Semantic naming:**
- **action-text** maps to `forest-green-primary`: Role "text" is grounded by usage context "Primary CTA button background, brand accent, shadow color variable, key link color".
- **action-background** maps to `page-white`: Role "background" is grounded by usage context "Main page background, button text on dark surfaces, ring offset color".
- **content-text** maps to `near-black-heading`: Role "text" is grounded by usage context "H1 heading text (probe-confirmed 72px), gradient-from variable".
- **surface-background** maps to `lime-tint-surface`: Role "background" is grounded by usage context "Light lime-tinted section backgrounds, subtle surface fills (78 hits)".

### Primary Brand
- **Border Gray** (#e5e7eb): Default border color across all components — highest count (326 hits), probe-confirmed borderColor. Role: primary. {authored: rgb(229, 231, 235), space: rgb}

### Text Scale
- **Amber Accent** (#e9be51): Logo accent mark (shovel blade highlight), decorative icon fills. Role: text. {authored: rgb(233, 190, 81), space: rgb}
- **Dark Forest Green** (#065f46): Navbar item link color (probe-confirmed), hover/active state for nav items. Role: text. {authored: rgb(6, 95, 70), space: rgb}
- **Deep Navy Text** (#101727): Primary body text, navigation links, footer text — highest frequency text color (97 hits). Role: text. {authored: rgb(16, 23, 39), space: rgb}
- **Forest Green Primary** (#01654d): Primary CTA button background, brand accent, shadow color variable, key link color. Role: text. {authored: rgb(1, 101, 77), space: rgb}
- **Light Amber** (#fcd34d): Warm yellow icon fills, illustration accents. Role: text. {authored: rgb(252, 211, 77), space: rgb}
- **Mid Gray Text** (#4b5563): Secondary body text, subheadings, descriptive copy. Role: text. {authored: rgb(75, 85, 99), space: rgb}
- **Muted Gray** (#9ca3af): Placeholder text, disabled states, secondary metadata. Role: text. {authored: rgb(156, 163, 175), space: rgb}
- **Near Black Heading** (#111827): H1 heading text (probe-confirmed 72px), gradient-from variable. Role: text. {authored: rgb(17, 24, 39), space: rgb}

### Interactive
- **Light Border Gray** (#d1d5db): Lighter dividers, input borders, subtle separators. Role: border. {authored: rgb(209, 213, 219), space: rgb}

### Surface & Shadows
- **Lime Tint Surface** (#f7fee7): Light lime-tinted section backgrounds, subtle surface fills (78 hits). Role: background. {authored: rgb(247, 254, 231), space: rgb}
- **Page White** (#ffffff): Main page background, button text on dark surfaces, ring offset color. Role: background. {authored: rgb(255, 255, 255), space: rgb, alpha: 0.05}

## Typography

Typography uses Scandia across extracted hierarchy roles. Keep hierarchy mapped to these token rows before adding decorative type styles.

Uses Scandia throughout for a uniform feel. Weight range spans semi-bold, medium, regular. Sizes range from 12px to 72px.

### Font Roles
- **Headline Font**: Scandia
- **Body Font**: Scandia

### Type Scale Evidence
| Role | Font | Size | Weight | Line Height | Letter Spacing | Stack / Features | Notes |
|------|------|------|--------|-------------|----------------|------------------|-------|
| H1 hero headline — probe-confirmed 72px, tight negative tracking | Scandia | 72px | 600 | 72px | -1.8px | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Major section headings | Scandia | 48px | 600 | 48px | -1.2px | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Sub-section headings, card titles | Scandia | 30px | 600 | 36px | -0.75px | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Card and feature headings | Scandia | 20px | 500 | 32px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Hero body copy, introductory paragraphs | Scandia | 18px | 400 | 32px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Standard body text — most frequent tuple (152 hits) | Scandia | 16px | 400 | 24px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Paragraph text with relaxed line height | Scandia | 16px | 400 | 28px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Emphasized body copy, feature descriptions | Scandia | 16px | 500 | 24px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Button labels, nav items, compact labels | Scandia | 16px | 600 | 16px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Secondary labels, metadata, captions | Scandia | 14px | 400 | 24px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Tag labels, badge text, small CTAs | Scandia | 14px | 600 | 24px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |
| Fine print, footnotes, timestamps | Scandia | 12px | 400 | 16px | normal | Scandia, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif | Extracted token |

## Layout

Responsive system uses 3 breakpoint tier(s): tablet, desktop, wide.

This system uses a 4px base grid with scale values 2, 4, 6, 8, 12, 16, 20, 24, 32, 36, 40, 64, 96, 128.

### Responsive Strategy
- **tablet (>= 640px)**: Increase spacing and column structure for medium-width viewports.
- **desktop (>= 1024px)**: Expand layout density and horizontal composition for wide viewports.
- **wide (>= 1536px)**: Stretch composition with generous gutters and wider layout spans.

### Spacing System
| Token | Value | Px | Notes |
|------|-------|----|-------|
| spacing-2 | 8px | 8 | Extracted spacing token |
| spacing-3 | 12px | 12 | Extracted spacing token |
| spacing-4 | 16px | 16 | Extracted spacing token |
| spacing-5 | 20px | 20 | Extracted spacing token |
| spacing-6 | 24px | 24 | Extracted spacing token |
| spacing-8 | 32px | 32 | Extracted spacing token |
| spacing-9 | 36px | 36 | Extracted spacing token |
| spacing-10 | 40px | 40 | Extracted spacing token |
| spacing-16 | 64px | 64 | Extracted spacing token |
| spacing-24 | 96px | 96 | Extracted spacing token |
| spacing-32 | 128px | 128 | Extracted spacing token |

## Elevation & Depth

Keep depth flat unless validated shadow or interaction evidence appears in the extraction payload. Do not invent shadows beyond this evidence boundary.

### Shadow Evidence
| Shadow Token | Layers | Details |
|--------------|--------|---------|
| input-ring | 3 | inset 0px 0px 0px 0px rgb(255, 255, 255) |
| input-ring-subtle | 3 | inset 0px 0px 0px 0px rgb(255, 255, 255) |
| shadow-xs | 3 | 0px 0px 0px 0px rgba(0, 0, 0, 0) |

### Interaction Signals
| Theme | Signal | Evidence |
|-------|--------|----------|
| Light | outline-color | rgb(16, 23, 39) ; rgb(247, 254, 231) ; rgb(17, 24, 39) |
| Light | outline-width | 3px |
| Light | outline-offset | 0px |
| Light | transform | matrix(1, 0, 0, 1, 0, 0) |

## Shapes

Shape language maps directly to rounded tokens. Keep component corners consistent with the role mapping below before introducing bespoke geometry.

### Radius Roles
| Token | Value | Px | Role Mapping |
|------|-------|----|--------------|
| radius-sm | 6px | 6 | Subtle corner |
| radius-md | 8px | 8 | Control corner |
| radius-lg | 16px | 16 | Card corner |
| radius-full | 9999px | 9999 | Large surface corner |

### Geometry Evidence
| Radius Token | Shape | Units |
|--------------|-------|-------|
| radius-sm | 6px | px |
| radius-md | 8px | px |
| radius-lg | 16px | px |
| radius-full | 9999px | px |

## Components

(none detected)

## Do's and Don'ts

Guardrails protect Single-family weight hierarchy, Soft, rounded geometry, Layered elevation without adding unsupported visual claims.

| Do | Don't |
|----|---------|
| Do maintain consistent spacing using the base grid | Don't make unsupported claims about absent visual features |
| Do maintain WCAG AA contrast ratios (4.5:1 for normal text) | Don't mix rounded and sharp corners in the same view |
| Do use the primary color only for the single most important action per screen |  |
| Do verify evidence before writing new design-system guidance |  |

## Responsive Evidence

### Breakpoints
| Name | Width | Key Changes |
|------|-------|-------------|
| Mobile | >= 640px | (min-width: 640px) |
| Tablet | >= 768px | (min-width: 768px) |
| Desktop | >= 1024px | (min-width: 1024px) |
| Desktop | >= 1280px | (min-width: 1280px) |
| Desktop | >= 1536px | (min-width: 1536px) |
| Breakpoint 6 | Unknown | (forced-colors: active) |

## Agent Prompt Guide

### Example Component Prompts
- Create button component using validated primary color role and spacing tokens.
- Create card component with mapped radius role and evidence-backed elevation.
- Create form input component using inferred typography hierarchy and border roles.

### Iteration Guide
1. Start with extracted palette and typography roles only.
2. Map spacing and radius directly from token tables before visual polish.
3. Apply component patterns one section at a time and compare against source intent.
4. Keep elevation claims tied to explicit evidence in output.
5. Iterate with smallest diffs and re-check section hierarchy after each change.
