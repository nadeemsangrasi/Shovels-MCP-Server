# shadcn/ui Components List

## All Available Components

### Form Components

**button** - Clickable button with variants
```bash
npx shadcn@latest add button
```

**input** - Text input field
```bash
npx shadcn@latest add input
```

**label** - Form label
```bash
npx shadcn@latest add label
```

**checkbox** - Checkbox input
```bash
npx shadcn@latest add checkbox
```

**radio-group** - Radio button group
```bash
npx shadcn@latest add radio-group
```

**select** - Dropdown select
```bash
npx shadcn@latest add select
```

**switch** - Toggle switch
```bash
npx shadcn@latest add switch
```

**textarea** - Multi-line text input
```bash
npx shadcn@latest add textarea
```

**form** - Form wrapper with validation
```bash
npx shadcn@latest add form
```

**slider** - Range slider input
```bash
npx shadcn@latest add slider
```

### Layout Components

**card** - Container card component
```bash
npx shadcn@latest add card
```

**separator** - Visual divider
```bash
npx shadcn@latest add separator
```

**tabs** - Tabbed interface
```bash
npx shadcn@latest add tabs
```

**accordion** - Expandable sections
```bash
npx shadcn@latest add accordion
```

**collapsible** - Collapsible content
```bash
npx shadcn@latest add collapsible
```

**aspect-ratio** - Maintain aspect ratio
```bash
npx shadcn@latest add aspect-ratio
```

**scroll-area** - Custom scrollbar
```bash
npx shadcn@latest add scroll-area
```

### Overlay Components

**dialog** - Modal dialog
```bash
npx shadcn@latest add dialog
```

**dropdown-menu** - Dropdown menu
```bash
npx shadcn@latest add dropdown-menu
```

**popover** - Popover overlay
```bash
npx shadcn@latest add popover
```

**sheet** - Slide-out panel
```bash
npx shadcn@latest add sheet
```

**tooltip** - Hover tooltip
```bash
npx shadcn@latest add tooltip
```

**context-menu** - Right-click menu
```bash
npx shadcn@latest add context-menu
```

**hover-card** - Hover card
```bash
npx shadcn@latest add hover-card
```

**alert-dialog** - Alert modal
```bash
npx shadcn@latest add alert-dialog
```

**command** - Command palette
```bash
npx shadcn@latest add command
```

**menubar** - Menu bar
```bash
npx shadcn@latest add menubar
```

**navigation-menu** - Navigation menu
```bash
npx shadcn@latest add navigation-menu
```

### Data Display

**table** - Data table
```bash
npx shadcn@latest add table
```

**badge** - Status badge
```bash
npx shadcn@latest add badge
```

**avatar** - User avatar
```bash
npx shadcn@latest add avatar
```

**progress** - Progress bar
```bash
npx shadcn@latest add progress
```

**calendar** - Date picker calendar
```bash
npx shadcn@latest add calendar
```

**data-table** - Advanced data table
```bash
npx shadcn@latest add data-table
```

### Feedback Components

**alert** - Alert message
```bash
npx shadcn@latest add alert
```

**toast** - Toast notification
```bash
npx shadcn@latest add toast
```

**skeleton** - Loading skeleton
```bash
npx shadcn@latest add skeleton
```

**sonner** - Toast notifications (Sonner)
```bash
npx shadcn@latest add sonner
```

### Utility Components

**breadcrumb** - Breadcrumb navigation
```bash
npx shadcn@latest add breadcrumb
```

**pagination** - Pagination controls
```bash
npx shadcn@latest add pagination
```

**resizable** - Resizable panels
```bash
npx shadcn@latest add resizable
```

**carousel** - Image carousel
```bash
npx shadcn@latest add carousel
```

**drawer** - Bottom drawer
```bash
npx shadcn@latest add drawer
```

**sidebar** - Sidebar navigation
```bash
npx shadcn@latest add sidebar
```

## Quick Add Common Sets

### Authentication UI
```bash
npx shadcn@latest add button input label card form
```

### Dashboard
```bash
npx shadcn@latest add card table tabs badge avatar
```

### Forms
```bash
npx shadcn@latest add form input label select checkbox radio-group switch textarea
```

### Overlays
```bash
npx shadcn@latest add dialog dropdown-menu popover sheet tooltip
```

### Data Display
```bash
npx shadcn@latest add table badge avatar progress skeleton
```

### Complete Starter Set
```bash
npx shadcn@latest add button input label card dialog dropdown-menu toast form
```

## Component Categories

### Essential (Start Here)
- button
- card
- input
- label

### Forms (Add for forms)
- form
- select
- checkbox
- radio-group
- switch
- textarea

### Navigation (Add for navigation)
- tabs
- navigation-menu
- menubar
- breadcrumb

### Overlays (Add for modals/menus)
- dialog
- dropdown-menu
- popover
- sheet

### Feedback (Add for notifications)
- toast
- alert
- skeleton

### Data (Add for tables/lists)
- table
- data-table
- avatar
- badge

## Component Dependencies

Some components require others:

**form** requires:
- label
- input (and other form components)

**data-table** requires:
- table
- checkbox (for selection)
- dropdown-menu (for actions)

**toast** requires:
- Configuration in layout

**command** requires:
- dialog
- popover

## Usage Examples

### Add Single Component
```bash
npx shadcn@latest add button
```

### Add Multiple Components
```bash
npx shadcn@latest add button card input label
```

### Add with Overwrite
```bash
npx shadcn@latest add button --overwrite
```

### List All Available
```bash
npx shadcn@latest add
```

## Component Locations

After adding, components are located at:
```
components/
└── ui/
    ├── button.tsx
    ├── card.tsx
    ├── input.tsx
    └── ...
```

## Customization

All components can be customized by editing the files in `components/ui/`. They are in your codebase, giving you full control.

## TypeScript

All components include full TypeScript definitions. Import and use with complete type safety:

```typescript
import { Button } from "@/components/ui/button"
import type { ButtonProps } from "@/components/ui/button"
```

## Accessibility

All components are built on Radix UI primitives, ensuring WCAG compliance and keyboard navigation support out of the box.
