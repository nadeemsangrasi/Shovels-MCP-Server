# Progressive Disclosure Guide for Skills

## Critical Rule: SKILL.md Line Limits

**Target:** < 500 lines
**Soft Maximum:** ~1,000 lines
**Hard Token Limit:** ~5,000 tokens (approximately 1,250-1,500 lines)

## Why These Limits?

1. **Context Window Efficiency**: When a skill activates, the entire SKILL.md is loaded into Claude's context. Keeping it under 5k tokens ensures efficient loading.

2. **Readability**: Longer files become harder for Claude to parse and follow accurately.

3. **Progressive Disclosure**: The whole point of skills is to load information progressively—SKILL.md should contain the workflow, not all the details.

## Proper Structure (The Pattern)

```
my-skill/
├── SKILL.md (300-500 lines)        ⚡ Core workflow - ALWAYS loaded
│   └─→ Essential steps, key patterns, references to other files
│
├── README.md                        📖 Documentation for users
│   └─→ Installation, usage, overview
│
├── references/                      🔍 On-demand loading
│   ├── quick-reference.md           → Common code snippets
│   ├── examples.md                  → Complete project patterns
│   ├── troubleshooting.md           → Error solutions
│   └── official-docs/               → Deep documentation
│       ├── topic-1.md
│       ├── topic-2.md
│       └── topic-3.md
│
├── scripts/                         🔧 Executable automation
│   └── helper-script.py
│
└── assets/                          📦 Templates, configs
    └── template.json
```

## What Goes in SKILL.md (Core Workflow)

### ✅ Include:
- **Overview** - Brief description (2-3 sentences)
- **When to Use** - Clear trigger conditions
- **Prerequisites** - Required setup
- **Instructions** - Core workflow steps (numbered phases)
  - Each step: action + validation
  - Minimal code examples (2-5 lines)
  - References to detailed docs
- **Common Patterns** - 3-5 most frequent use cases (brief)
- **Error Handling** - Quick error table with solutions
- **Decision Trees** - Flow charts for choices
- **References** - Links to detailed docs in `references/`

### ❌ Exclude (Move to references/):
- Long code examples (> 10 lines)
- Multiple variations of same pattern
- Detailed explanations
- Complete API documentation
- Extensive troubleshooting
- Full project examples
- Deep dives into concepts

## Pattern in Action

### ❌ Bad SKILL.md (Too Detailed)

```markdown
## Instructions

### Step 1: Create Component

Create a React component with the following code:

```typescript
import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

interface User {
  id: string
  name: string
  email: string
}

export function UserProfile() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    async function fetchUser() {
      try {
        const response = await axios.get(`/api/users/${router.query.id}`)
        setUser(response.data)
      } catch (error) {
        console.error('Failed to fetch user:', error)
      } finally {
        setLoading(false)
      }
    }

    if (router.query.id) {
      fetchUser()
    }
  }, [router.query.id])

  if (loading) return <div>Loading...</div>
  if (!user) return <div>User not found</div>

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

This is 962 lines of detailed code examples!
```

### ✅ Good SKILL.md (Concise + References)

```markdown
## Instructions

### Step 1: Create Component

**Quick pattern:**
```typescript
export function Component() {
  const [state, setState] = useState(null)
  // Fetch data, handle loading/error
  return <div>{/* UI */}</div>
}
```

**See:** `references/examples.md#user-profile` for complete implementation

**Key points:**
- Use TypeScript for type safety
- Handle loading and error states
- Fetch data in useEffect

**Validation:**
- [ ] Component renders without errors
- [ ] Loading state displays correctly
- [ ] Error handling works

This is 501 lines with references to detailed docs!
```

## Reference File Organization

### references/quick-reference.md
**Purpose:** Fast lookup for common code snippets
**Content:** Copy-paste ready code patterns
**Length:** Any (typically 500-1000 lines)

```markdown
# Quick Reference

## Basic Component
```typescript
export function Component() {
  return <div>Hello</div>
}
```

## Component with State
```typescript
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

(Many more snippets...)
```

### references/examples.md
**Purpose:** Complete, production-ready examples
**Content:** Full implementations with context
**Length:** Any (typically 800-2000 lines)

```markdown
# Complete Examples

## Example 1: User Profile System

### Project Structure
```
app/
├── users/
│   ├── page.tsx
│   └── [id]/
│       └── page.tsx
```

### Implementation

**User List Page:**
```typescript
// Complete 40-line implementation
```

**User Detail Page:**
```typescript
// Complete 60-line implementation
```

(Multiple complete examples...)
```

### references/troubleshooting.md
**Purpose:** Common errors and solutions
**Content:** Error messages, causes, fixes
**Length:** Any (typically 500-1000 lines)

```markdown
# Troubleshooting

## Error: "Cannot find module"

**Symptoms:**
```
Error: Cannot find module '@/components/Button'
```

**Cause:** Incorrect import path or tsconfig issue

**Solution:**
1. Check import path case sensitivity
2. Verify tsconfig.json paths configuration
3. Restart TypeScript server

(Many more errors...)
```

### references/official-docs/
**Purpose:** Deep documentation from official sources
**Content:** Comprehensive guides, fetched via Context7
**Length:** Any (can be very long)

```
official-docs/
├── data-fetching.md      (500 lines)
├── routing.md            (700 lines)
├── components.md         (800 lines)
└── server-actions.md     (900 lines)
```

## Token Efficiency Analysis

### Before Progressive Disclosure
```
Skill activation loads:
  SKILL.md: 962 lines (~2,400 tokens)

Total initial context: ~2,400 tokens
```

### After Progressive Disclosure
```
Skill activation loads:
  SKILL.md: 501 lines (~1,250 tokens)

Reference docs (5,112 lines):
  - Only loaded when Claude needs them
  - On-demand, not on activation

Total initial context: ~1,250 tokens
Savings: 48% reduction!
```

## How Claude Uses References

### Automatic Reference Loading

When user asks: "Show me a complete authentication example"

**Claude's process:**
1. SKILL.md loaded (already in context)
2. Sees reference: `references/examples.md#authentication`
3. Uses Read tool to load that specific section
4. Returns complete example to user
5. Reference unloads after use (not kept in context)

### Smart Referencing in SKILL.md

```markdown
## Phase 3: Implement Authentication

**Quick steps:**
1. Create login form
2. Add server action
3. Set session cookie

**See:** `references/examples.md#authentication` for complete implementation

**See:** `references/official-docs/server-actions.md` for action patterns

**See:** `references/troubleshooting.md#auth-errors` if errors occur
```

This way:
- SKILL.md stays concise
- User gets complete information when needed
- Context stays efficient

## Real Example: Next.js 16 Skill

### Before Optimization
```
SKILL.md: 962 lines
  - Long code examples
  - Multiple complete projects
  - Extensive troubleshooting
  - Deep explanations

Result: Too large, slow to load
```

### After Optimization
```
SKILL.md: 501 lines ✅
  - Core workflow only
  - Minimal examples
  - References to detailed docs

references/examples.md: 921 lines
  - 4 complete project examples
  - Blog, Dashboard, E-commerce, Auth

references/quick-reference.md: 660 lines
  - Common code snippets
  - Decision trees
  - Pattern cheat sheet

references/troubleshooting.md: 701 lines
  - 10+ common errors
  - Solutions with examples
  - Debug tips

references/official-docs/: 2,830 lines
  - Data fetching (494 lines)
  - Routing (732 lines)
  - Components (730 lines)
  - Server actions (874 lines)

Total: 6,613 lines
Initial load: Only 501 lines!
Efficiency: 48% reduction in initial context
```

## Optimization Checklist

When creating a new skill:

**1. Write SKILL.md first (aim for 300-500 lines):**
- [ ] Overview and trigger conditions
- [ ] Prerequisites
- [ ] Core workflow (numbered steps)
- [ ] Minimal code examples (< 10 lines each)
- [ ] References to detailed docs
- [ ] Quick error table
- [ ] Decision trees

**2. If SKILL.md exceeds 500 lines, extract:**
- [ ] Long code examples → `references/examples.md`
- [ ] Common snippets → `references/quick-reference.md`
- [ ] Error solutions → `references/troubleshooting.md`
- [ ] Deep dives → `references/official-docs/*.md`

**3. In SKILL.md, add clear references:**
```markdown
**See:** `references/examples.md#section-name`
**See:** `references/quick-reference.md`
**See:** `references/troubleshooting.md#error-name`
```

**4. Validate:**
- [ ] SKILL.md < 500 lines (501 acceptable)
- [ ] Each step references detailed docs
- [ ] Examples are minimal (2-10 lines)
- [ ] All sections present
- [ ] References are clear

## Common Mistakes

### ❌ Mistake 1: All Content in SKILL.md
```markdown
SKILL.md: 1,500 lines
  - Everything in one file
  - No references/
  - Claude loads 1,500 lines every activation
```

### ❌ Mistake 2: Vague References
```markdown
**See the examples file for more information**

Claude: Which examples file? Where?
```

### ❌ Mistake 3: No Examples at All
```markdown
SKILL.md: 200 lines (very concise)
  - But no examples anywhere!
  - User asks: "Show me an example"
  - Claude: "No examples available"
```

### ✅ Correct Pattern
```markdown
SKILL.md: 450 lines
  - Core workflow
  - Minimal examples (5 lines)
  - Clear references: `references/examples.md#user-auth`

references/examples.md: 800 lines
  - Complete implementations
  - Multiple variations
  - Production-ready code
```

## Summary: The Rule

**SKILL.md = Workflow + References**
**references/ = Details + Examples + Docs**

**Target:**
- SKILL.md: < 500 lines
- Reference docs: Unlimited (loaded on-demand)

**Benefits:**
- Fast skill activation
- Efficient context usage
- Complete information available
- Better user experience

**Remember:** Progressive disclosure is about loading information progressively, not hiding it. All information should be available, just not all loaded at once.

## Quick Formula

```
SKILL.md size = Overview (20 lines)
              + Prerequisites (20 lines)
              + Instructions (300 lines)
                - Core steps only
                - Mini examples (2-5 lines)
                - References to details
              + Common Patterns (50 lines)
              + Error Handling (30 lines)
              + Decision Trees (30 lines)
              + References (20 lines)
              + Tips (30 lines)
              = ~500 lines ✅

Everything else → references/ (loaded on-demand)
```

This is the pattern that should be followed for EVERY skill creation!
