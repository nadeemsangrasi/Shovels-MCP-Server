# Next.js 16 Development Skill

A comprehensive Claude Code skill for building Next.js 16 applications with App Router, Server Components, Server Actions, and modern React features.

## Overview

This skill provides step-by-step guidance for developing Next.js 16 applications, leveraging the Context7 MCP server to access up-to-date official documentation. It covers everything from project setup to advanced patterns, ensuring you follow current best practices.

## Features

- **Next.js 16 App Router**: File-system based routing with layouts and nested routes
- **Server Components**: Default server-side rendering with selective client components
- **Server Actions**: Direct server-side mutations without API routes
- **Data Fetching**: Multiple caching strategies for optimal performance
- **Forms & Validation**: Progressive enhancement with built-in form handling
- **Error Handling**: Comprehensive error boundaries and loading states
- **Context7 Integration**: Access official Next.js documentation on demand

## Installation

Copy this skill directory to your Claude Code skills location:

```bash
# For project-specific skills
cp -r nextjs16 .claude/skills/

# For personal skills (available across all projects)
cp -r nextjs16 ~/.claude/skills/
```

## Prerequisites

### Required
- Node.js 18.17 or later
- npm, yarn, or pnpm package manager
- Context7 MCP server configured
- Basic understanding of React

### Recommended
- TypeScript knowledge
- Understanding of async/await patterns

## Usage

### Activation

The skill activates automatically when you use trigger keywords:

```
"Create a Next.js 16 application with..."
"Build a Next.js app with Server Components"
"Implement Server Actions for form handling"
"Set up App Router with nested layouts"
```

Or explicitly:

```
"Use the nextjs16 skill to build an e-commerce site"
```

### Common Tasks

**Create New Project:**
```
"Create a new Next.js 16 project with TypeScript"
```

**Add Features:**
```
"Add a blog with dynamic routes and data fetching"
"Implement user authentication with Server Actions"
"Create a dashboard with real-time data"
```

**Reference Documentation:**
```
"Show me Next.js 16 documentation for data fetching"
"What are the best practices for Server Components?"
```

## Structure

```
nextjs16/
├── SKILL.md                              # Main skill instructions
├── README.md                              # This file
├── references/
│   └── official-docs/
│       ├── data-fetching.md              # Data fetching patterns
│       ├── routing.md                     # Routing and file conventions
│       ├── components.md                  # Server/Client Components
│       └── server-actions.md              # Server Actions guide
├── scripts/                               # (Reserved for future automation)
└── assets/                                # (Reserved for templates)
```

## Documentation

### Quick Reference

The skill includes comprehensive reference documentation:

- **Data Fetching** (`references/official-docs/data-fetching.md`)
  - Static, dynamic, and revalidated fetching
  - Caching strategies
  - Error handling
  - Request deduplication

- **Routing** (`references/official-docs/routing.md`)
  - App Router file conventions
  - Dynamic routes and layouts
  - Loading and error states
  - Navigation patterns

- **Components** (`references/official-docs/components.md`)
  - Server vs Client Components
  - Composition patterns
  - When to use each type
  - Best practices

- **Server Actions** (`references/official-docs/server-actions.md`)
  - Form handling
  - Data mutations
  - Revalidation
  - Authentication examples

### Context7 Integration

The skill uses Context7 MCP to fetch official Next.js documentation:

```
Library ID: /vercel/next.js/v16.1.0
```

Claude will automatically query Context7 when you need specific documentation or clarification on Next.js features.

## Examples

### Create a Blog

```
"Use the nextjs16 skill to create a blog with:
- Home page listing all posts
- Dynamic routes for individual posts
- Static generation with revalidation
- Markdown content support"
```

### Build a Dashboard

```
"Build a Next.js dashboard with:
- Server Components for data fetching
- Client Components for charts
- Real-time data updates
- Loading skeletons"
```

### Implement Authentication

```
"Add user authentication with:
- Server Actions for signup/login
- Protected routes
- Session management
- Redirect after login"
```

## Configuration

### Next.js Config

The skill guides you through configuring:
- TypeScript
- ESLint
- Tailwind CSS (optional)
- Image optimization
- Environment variables

### Context7 MCP

Ensure Context7 MCP server is configured in your Claude Code settings to enable documentation fetching.

## Best Practices

The skill enforces Next.js 16 best practices:

1. **Server Components First**: Start with Server Components (default)
2. **Client Components When Needed**: Only add `'use client'` for interactivity
3. **Appropriate Caching**: Choose the right strategy for your data
4. **Error Boundaries**: Add loading and error states
5. **Type Safety**: Use TypeScript for better DX

## Troubleshooting

### Skill Not Loading

1. Verify file location: `.claude/skills/nextjs16/SKILL.md`
2. Check YAML frontmatter syntax
3. Restart Claude Code

### Skill Not Activating

1. Use trigger keywords: "Next.js", "App Router", "Server Components"
2. Explicitly mention: "Use the nextjs16 skill"

### Documentation Not Available

1. Verify Context7 MCP server is running
2. Check network connectivity
3. Fall back to local reference docs in `references/`

## Version History

### v1.0.0 (2026-01-01)
- Initial release
- Next.js 16.1.0 support
- Complete App Router coverage
- Server Components and Server Actions
- Context7 documentation integration
- Comprehensive examples and patterns

## Contributing

To improve this skill:

1. Add new examples to SKILL.md
2. Update reference docs with new patterns
3. Create automation scripts for common tasks
4. Add templates for project structures

## License

MIT License - This skill is provided as-is for use with Claude Code.

## Resources

- **Official Docs**: https://nextjs.org/docs
- **Next.js GitHub**: https://github.com/vercel/next.js
- **Context7 Library**: `/vercel/next.js/v16.1.0`
- **Examples**: https://github.com/vercel/next.js/tree/canary/examples

## Support

For issues with:
- **This skill**: Create an issue in your project repository
- **Next.js**: Check official documentation or GitHub issues
- **Claude Code**: Use `/help` command or visit Claude Code docs
- **Context7**: Check Context7 MCP server configuration

---

**Happy coding with Next.js 16!**
