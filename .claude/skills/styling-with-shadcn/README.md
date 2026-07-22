# Styling with shadcn/ui

A comprehensive Claude Code skill for building beautiful, accessible Next.js applications with shadcn/ui—a collection of re-usable components built with Radix UI and Tailwind CSS.

## Overview

shadcn/ui is not an NPM package but a CLI tool that adds components directly to your project. This gives you full control and ownership of the code, allowing complete customization without being tied to a package version.

**Key Features:**
- 50+ accessible UI components
- Built on Radix UI primitives
- Styled with Tailwind CSS
- Full TypeScript support
- Dark mode support
- Form validation with Zod
- Copy components into your codebase

## Installation

### Prerequisites

1. **Next.js 13+** with App Router
2. **Tailwind CSS** configured
3. **TypeScript** (recommended)
4. **Node.js 18+**

### Skill Installation

```bash
# Copy to project skills
cp -r styling-with-shadcn /path/to/project/.claude/skills/

# Or copy to global skills
cp -r styling-with-shadcn ~/.claude/skills/
```

## Usage

### Activation

The skill activates with trigger keywords:
- "shadcn"
- "shadcn/ui"
- "ui components"
- "style nextjs"
- "add button"
- "dark mode"
- "theming"

### Quick Start

```bash
# 1. Initialize shadcn/ui
npx shadcn@latest init

# 2. Add your first component
npx shadcn@latest add button

# 3. Use in your app
import { Button } from "@/components/ui/button"
<Button>Click me</Button>
```

### Example Prompts

**Setup:**
- "Initialize shadcn/ui in my Next.js project"
- "Configure shadcn with dark mode support"

**Adding Components:**
- "Add button and card components"
- "Add form components with validation"
- "Add dialog and dropdown menu"

**Building UI:**
- "Create a login form with shadcn components"
- "Build a dashboard layout with cards and tables"
- "Implement a theme toggle"

**Customization:**
- "Customize button variants"
- "Change theme colors"
- "Add custom component styles"

## Documentation Structure

```
styling-with-shadcn/
├── SKILL.md (486 lines)              # Main workflow
├── README.md                          # This file
├── references/
│   ├── examples.md                    # Complete component examples
│   ├── components-list.md             # All available components
│   ├── installation-guide.md          # Detailed setup
│   ├── configuration.md               # Config options
│   ├── theming-guide.md               # Dark mode & themes
│   ├── forms-guide.md                 # Form validation
│   ├── customization-guide.md         # Styling components
│   ├── troubleshooting.md             # Common issues
│   └── integration-guides.md          # Use with other skills
└── scripts/
    └── init-shadcn.sh                 # Quick init script
```

## Components Available

### Form Components
- Button
- Input
- Label
- Checkbox
- Radio Group
- Select
- Switch
- Textarea
- Form (with validation)

### Layout Components
- Card
- Separator
- Tabs
- Accordion
- Collapsible

### Overlay Components
- Dialog
- Dropdown Menu
- Popover
- Sheet
- Tooltip

### Data Display
- Table
- Badge
- Avatar
- Progress

### Feedback
- Alert
- Toast
- Skeleton

**Full list:** See `references/components-list.md`

## Features

### ✅ Easy Installation
CLI tool adds components directly to your project

### ✅ Full Customization
Components live in your codebase—edit freely

### ✅ Accessibility
Built on Radix UI primitives for WCAG compliance

### ✅ Dark Mode
CSS variables for easy theming

### ✅ Form Validation
Integrated with react-hook-form and Zod

### ✅ TypeScript
Full type safety and IntelliSense

### ✅ Responsive
Mobile-first design with Tailwind CSS

## Common Use Cases

### Authentication UI
```typescript
// Login/signup forms with validation
import { Card, Input, Button, Label } from "@/components/ui/*"
```

### Dashboard Layouts
```typescript
// Cards, tables, tabs for data display
import { Card, Table, Tabs } from "@/components/ui/*"
```

### Forms with Validation
```typescript
// react-hook-form + Zod schemas
import { Form } from "@/components/ui/form"
```

### Settings Pages
```typescript
// Tabs, switches, selects for preferences
import { Tabs, Switch, Select } from "@/components/ui/*"
```

## Integration with Other Skills

### With better-auth-nextjs
- Use shadcn components for auth forms
- Style sign-in/sign-up pages
- Add validated form fields
- Implement consistent UI

### With nextjs-dev-tool
- Test components with browser automation
- Verify dark mode functionality
- Check form submissions
- Validate accessibility

### With nextjs16
- Build pages with shadcn components
- Use with Server Components
- Implement App Router layouts
- Style metadata pages

See `references/integration-guides.md` for detailed workflows.

## Best Practices

1. **Initialize first** - Run `init` before adding components
2. **Use TypeScript** - Full type safety prevents errors
3. **Validate forms** - Always use Zod schemas
4. **Enable CSS variables** - Better theming support
5. **Customize in place** - Edit components directly
6. **Test dark mode** - Implement early in development
7. **Follow accessibility** - Use semantic HTML
8. **Leverage examples** - Check official docs for patterns

## Troubleshooting

### Components not found
**Solution:** Run `npx shadcn@latest add <component>`

### Styles not applying
**Solution:** Verify Tailwind CSS is configured correctly

### Import errors
**Solution:** Check aliases in `components.json`

### Dark mode not working
**Solution:** Ensure ThemeProvider is set up

See `references/troubleshooting.md` for complete guide.

## Requirements

**Minimum:**
- Next.js 13.0.0+
- Tailwind CSS 3.0.0+
- React 18.0.0+
- Node.js 18.0.0+

**Recommended:**
- TypeScript 5.0.0+
- next-themes 0.2.0+ (for dark mode)
- react-hook-form 7.0.0+ (for forms)
- zod 3.0.0+ (for validation)

## Resources

**Official:**
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Components](https://ui.shadcn.com/docs/components)
- [Themes](https://ui.shadcn.com/themes)
- [Examples](https://ui.shadcn.com/examples)

**Local Documentation:**
- Complete examples: `references/examples.md`
- All components: `references/components-list.md`
- Setup guide: `references/installation-guide.md`
- Theming: `references/theming-guide.md`

## Version History

**v1.0.0 (2026-01-01)**
- Initial release
- 50+ components documented
- Dark mode theming support
- Form validation patterns
- Integration with Next.js skills
- Progressive disclosure structure (486 lines)

## Support

- [shadcn/ui GitHub](https://github.com/shadcn-ui/ui)
- [Discord Community](https://discord.gg/shadcn)
- [Twitter](https://twitter.com/shadcn)

## License

This skill integrates with:
- shadcn/ui (MIT License)
- Radix UI (MIT License)
- Tailwind CSS (MIT License)

## Contributing

Improvements welcome! Please ensure:
- SKILL.md stays under 500 lines
- Examples are complete and tested
- Documentation is clear
- Integration guides are updated

---

**Created with:** Claude Code + skill-creator + Context7 MCP
**Documentation Quality:** Production-ready
**Maintenance:** Self-contained, version 1.0.0
