---
name: styling-with-shadcn
description: Style Next.js applications with shadcn/ui component library. Install CLI, add accessible UI components, implement theming with Tailwind CSS, and build forms with validation. Use when adding styled components, implementing dark mode, or creating consistent UI in Next.js projects.
version: 1.0.0
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
author: Claude Code
tags: [shadcn, ui, styling, tailwind, nextjs, components, theming, dark-mode, forms, accessible]
---

# Styling with shadcn/ui

Build beautiful, accessible Next.js applications using shadcn/ui—a collection of re-usable components built with Radix UI and Tailwind CSS. Components are copied into your project for full control and customization.

## Overview

shadcn/ui is not an NPM package but a CLI tool that adds components directly to your codebase. Built on Radix UI primitives for accessibility and Tailwind CSS for styling, it provides 50+ production-ready components with full customization control.

## When to Use This Skill

**Activate when:**
- Setting up shadcn/ui in Next.js projects
- Adding UI components (buttons, forms, dialogs, cards)
- Implementing dark mode with theming
- Building accessible forms with validation
- Creating consistent design systems
- Customizing component styles

**Trigger keywords:** "shadcn", "shadcn/ui", "ui components", "style nextjs", "add button", "dark mode", "theming"

**NOT for:**
- Non-Next.js projects without adaptation
- Projects not using Tailwind CSS
- When you need a traditional component library package

## Prerequisites

**Required:**
- Next.js 13+ (App Router recommended)
- Tailwind CSS configured
- TypeScript (recommended)
- Node.js 18+

**Recommended:**
- Basic Tailwind CSS knowledge
- Understanding of React Server Components
- Git initialized (for tracking changes)

## Instructions

### Phase 1: Installation and Setup

#### Step 1: Install shadcn/ui CLI

**Quick:**
```bash
npx shadcn@latest init
```

**Interactive prompts:**
- Style: `Default` or `New York`
- Base color: `Zinc`, `Slate`, `Stone`, etc.
- CSS variables: `Yes` (recommended)

**See:** `references/installation-guide.md`

#### Step 2: Verify Configuration

**Check `components.json` created:**
```json
{
  "style": "default",
  "tailwind": {
    "cssVariables": true,
    "baseColor": "zinc"
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

**See:** `references/configuration.md`

#### Step 3: Check Tailwind Configuration

**Verify `tailwind.config.ts` updated:**
```typescript
// Should include content paths and theme extensions
```

**Check `globals.css` has CSS variables:**
```css
:root {
  --background: ...;
  --foreground: ...;
}
```

**See:** `references/configuration.md#tailwind-setup`

### Phase 2: Adding Components

#### Step 4: Add Your First Component

**Add a button:**
```bash
npx shadcn@latest add button
```

**Creates:**
- `components/ui/button.tsx`
- All necessary dependencies

**Use in your app:**
```typescript
import { Button } from "@/components/ui/button"

<Button>Click me</Button>
```

**See:** `references/components-reference.md#button`

#### Step 5: Add Multiple Components

**Quick:**
```bash
npx shadcn@latest add card input label form
```

**Adds all listed components at once**

**See:** `references/components-reference.md`

#### Step 6: Browse Available Components

**List all components:**
```bash
npx shadcn@latest add
```

**Common components:**
- button, input, label, form
- card, dialog, dropdown-menu
- table, tabs, toast
- select, checkbox, radio-group

**See:** `references/components-list.md`

### Phase 3: Building UI

#### Step 7: Create a Form

**Quick example:**
```typescript
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

<form>
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" />
  <Button type="submit">Submit</Button>
</form>
```

**See:** `references/examples.md#forms`

#### Step 8: Build a Card Layout

**Quick:**
```typescript
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>
```

**See:** `references/examples.md#cards`

#### Step 9: Add a Dialog

**Quick:**
```typescript
import { Dialog, DialogTrigger, DialogContent } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>Modal content</DialogContent>
</Dialog>
```

**See:** `references/examples.md#dialogs`

### Phase 4: Theming and Dark Mode

#### Step 10: Install Dark Mode Support

**Add next-themes:**
```bash
npm install next-themes
```

**Create theme provider:**
```typescript
// components/theme-provider.tsx
"use client"
import { ThemeProvider as NextThemesProvider } from "next-themes"

export function ThemeProvider({ children, ...props }) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}
```

**See:** `references/theming-guide.md#dark-mode`

#### Step 11: Wrap App with Theme Provider

**Update `app/layout.tsx`:**
```typescript
import { ThemeProvider } from "@/components/theme-provider"

<html suppressHydrationWarning>
  <body>
    <ThemeProvider attribute="class" defaultTheme="system">
      {children}
    </ThemeProvider>
  </body>
</html>
```

**See:** `references/theming-guide.md#setup`

#### Step 12: Add Theme Toggle

**Quick:**
```bash
npx shadcn@latest add dropdown-menu
```

**Create toggle component:**
```typescript
// components/theme-toggle.tsx
import { useTheme } from "next-themes"

// Toggle between light/dark/system
```

**See:** `references/examples.md#theme-toggle`

### Phase 5: Form Validation

#### Step 13: Add Form Component

**Install form support:**
```bash
npx shadcn@latest add form
npm install react-hook-form zod @hookform/resolvers
```

**See:** `references/forms-guide.md`

#### Step 14: Build Validated Form

**Quick:**
```typescript
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"

const schema = z.object({
  email: z.string().email()
})

// Use with Form component
```

**See:** `references/examples.md#validated-forms`

### Phase 6: Customization

#### Step 15: Customize Component Styles

**Components are in your codebase:**
```typescript
// Edit components/ui/button.tsx directly
// Modify Tailwind classes
// Add new variants
```

**See:** `references/customization-guide.md`

#### Step 16: Customize Theme Colors

**Update CSS variables in `globals.css`:**
```css
:root {
  --primary: oklch(...);
  --secondary: oklch(...);
}
```

**See:** `references/theming-guide.md#colors`

## Common Patterns

### Pattern 1: Quick Component Setup
**Quick:** `npx shadcn@latest add button card input`

**See:** `references/quick-start.md`

### Pattern 2: Form with Validation
**Quick:** Add form component + use react-hook-form + zod

**See:** `references/forms-guide.md#validated`

### Pattern 3: Dashboard Layout
**Quick:** Card + Table + Dialog components

**See:** `references/examples.md#dashboard`

### Pattern 4: Authentication UI
**Quick:** Card + Form + Button + Input

**See:** `references/examples.md#auth-ui`

### Pattern 5: Settings Page
**Quick:** Tabs + Form + Switch + Select

**See:** `references/examples.md#settings`

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Command not found | CLI not installed | Run `npx shadcn@latest` |
| Import errors | Wrong alias path | Check `components.json` aliases |
| Styles not applying | Tailwind not configured | Verify `tailwind.config.ts` |
| Dark mode not working | Provider not set up | Add ThemeProvider |
| Component not found | Not added yet | Run `npx shadcn@latest add <component>` |

**See:** `references/troubleshooting.md`

## Component Categories

**Form Components:**
- Button, Input, Label, Checkbox, Radio, Select, Switch, Textarea

**Layout Components:**
- Card, Separator, Tabs, Accordion, Collapsible

**Overlay Components:**
- Dialog, Dropdown Menu, Popover, Sheet, Tooltip

**Data Display:**
- Table, Badge, Avatar, Progress

**Feedback:**
- Alert, Toast, Skeleton

**See:** `references/components-list.md`

## Integration with Other Skills

### With better-auth-nextjs
Use shadcn/ui for auth forms:
- Card for login/signup containers
- Form components with validation
- Input for email/password fields
- Button for submit actions

### With nextjs-dev-tool
- Use browser_eval to test UI components
- Verify dark mode works correctly
- Test form submissions
- Check accessibility

**See:** `references/integration-guides.md`

## Best Practices

1. **Use CSS variables** - Enable `cssVariables: true` in config
2. **Customize in place** - Edit components directly in your codebase
3. **Consistent spacing** - Use Tailwind spacing scale
4. **Accessibility first** - Built on Radix UI primitives
5. **Type safety** - Use TypeScript for all components
6. **Dark mode support** - Implement from the start
7. **Form validation** - Always use schema validation (zod)

## Validation Checklist

**Setup:**
- [ ] shadcn/ui CLI initialized
- [ ] `components.json` created
- [ ] Tailwind CSS configured
- [ ] CSS variables set up
- [ ] Aliases configured

**Functionality:**
- [ ] Components render correctly
- [ ] Styles apply properly
- [ ] Dark mode works
- [ ] Forms validate
- [ ] TypeScript types resolve

**Production Ready:**
- [ ] All components customized
- [ ] Theme colors configured
- [ ] Accessibility tested
- [ ] Responsive design verified

## Quick Reference

**Add component:**
```bash
npx shadcn@latest add <component-name>
```

**Add multiple:**
```bash
npx shadcn@latest add button card input form
```

**Update component:**
```bash
npx shadcn@latest add <component-name> --overwrite
```

**List components:**
```bash
npx shadcn@latest add
```

## References

**Local Documentation:**
- Installation guide: `references/installation-guide.md`
- Configuration: `references/configuration.md`
- Components reference: `references/components-reference.md`
- Components list: `references/components-list.md`
- Examples: `references/examples.md`
- Forms guide: `references/forms-guide.md`
- Theming guide: `references/theming-guide.md`
- Customization: `references/customization-guide.md`
- Troubleshooting: `references/troubleshooting.md`
- Integration guides: `references/integration-guides.md`
- Quick start: `references/quick-start.md`

**External Resources:**
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Components](https://ui.shadcn.com/docs/components)
- [Theming](https://ui.shadcn.com/docs/theming)
- [Dark Mode](https://ui.shadcn.com/docs/dark-mode)

## Tips for Success

1. **Initialize first** - Run `init` before adding components
2. **Check config** - Verify `components.json` paths match your structure
3. **Customize freely** - Components are in your codebase, edit them
4. **Use examples** - Check official docs for usage patterns
5. **Type everything** - TypeScript catches issues early
6. **Test dark mode** - Implement early, test throughout
7. **Validate forms** - Always use zod schemas
8. **Leverage Context7** - Query docs for specific component usage

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- Next.js 13+ support
- 50+ components documented
- Dark mode theming
- Form validation patterns
- Integration guides
- Progressive disclosure structure

## Sources

- [shadcn/ui Official Documentation](https://ui.shadcn.com)
- [Context7: shadcn/ui](https://context7.com)
- [Radix UI](https://www.radix-ui.com)
- [Tailwind CSS](https://tailwindcss.com)
