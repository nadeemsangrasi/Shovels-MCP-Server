---
name: skill-creator
description: Create new Claude Code skills with proper structure, validation, and best practices. Use when building custom skills, generating skill templates, or setting up skill workflows. Handles YAML frontmatter, progressive disclosure, script generation, and documentation.
version: 2.0.0
allowed-tools: Bash, Read, Write, Grep, Glob, mcp__context7__query-docs, mcp__context7__resolve-library-id
author: SpecKit Plus
tags: [skills, templates, automation, development]
---

# Skill Creator

## Overview

Create well-structured Claude Code skills following best practices. Automates skill directory creation, SKILL.md files with proper YAML frontmatter, supporting scripts, reference documentation, and validation checks.

**⚠️ CRITICAL: All skills MUST follow progressive disclosure - SKILL.md < 500 lines!**

**📖 See:** `references/progressive-disclosure-guide.md` for complete pattern with examples

## When to Use This Skill

**Activate when:**
- Creating new Claude Code skill from scratch
- Generating skill templates
- Setting up skill structure with scripts/references
- Validating existing skills
- Converting workflows into reusable skills

**Trigger keywords:** "create skill", "new skill", "skill template", "build skill"

## Prerequisites

**Required:**
- Claude Code installed
- Write access to `.claude/skills/` or `~/.claude/skills/`
- Understanding of progressive disclosure

**Optional:**
- Python 3.8+ (for scripts)
- Context7 MCP (for tech documentation)

## Instructions

### Phase 1: Planning (Define Skill Requirements)

#### Step 1: Gather Core Information

**Required:**
1. **Name**: lowercase-with-hyphens, max 64 chars
2. **Description**: action-oriented, trigger keywords, max 1024 chars
3. **Purpose**: problem it solves
4. **Triggers**: when Claude should activate it
5. **Workflow**: main execution phases

**Validation questions:**
- Repeated 5+ times? (if no, may not need skill)
- Can break into clear steps?
- Has specific trigger keywords?

**See:** `references/skill-planning-guide.md` for detailed requirements gathering

#### Step 2: Understand Progressive Disclosure (MANDATORY!)

**⚠️ THE RULE: SKILL.md < 500 lines**

**Structure:**
```
SKILL.md (300-500 lines) ⚡ Core workflow
  ├─ Overview (brief)
  ├─ Prerequisites
  ├─ Instructions (essential steps + mini examples)
  ├─ Common Patterns (3-5 brief)
  └─ References to detailed docs

references/ (unlimited) 🔍 Loaded on-demand
  ├─ examples.md           → Complete implementations
  ├─ quick-reference.md    → Code snippets
  ├─ troubleshooting.md    → Error solutions
  └─ official-docs/        → Deep documentation
```

**Mini example pattern:**
```markdown
### Step 5: Create Component

**Quick:**
```typescript
export function Component() { return <div>Hello</div> }
```

**See:** `references/examples.md#complete-component`
```

**📖 REQUIRED:** Read `references/progressive-disclosure-guide.md` before proceeding!

### Phase 2: Structure Creation

#### Step 3: Create Skill Directory

**Quick:**
```bash
mkdir -p .claude/skills/skill-name/{scripts,references/official-docs,assets}
```

**Structure:**
```
skill-name/
├── SKILL.md           # Core workflow (< 500 lines)
├── README.md          # Installation guide
├── scripts/           # Automation
├── references/        # Detailed docs (unlimited)
│   ├── examples.md
│   ├── quick-reference.md
│   ├── troubleshooting.md
│   └── official-docs/
└── assets/           # Templates, configs
```

**See:** `references/skill-creation-workflow.md#directory-structure`

#### Step 4: Create SKILL.md with Frontmatter

**Template:**
```yaml
---
name: skill-name
description: Clear, action-oriented with trigger keywords (max 1024 chars)
version: 1.0.0
allowed-tools: Bash, Read, Write
author: Your Name
tags: [category1, category2]
---
```

**Required sections in SKILL.md:**
- Overview (brief description)
- When to Use (trigger conditions)
- Prerequisites
- Instructions (core workflow with mini examples)
- Common Patterns (3-5 brief)
- Error Handling (quick table)
- References (links to detailed docs)

**See:** `references/skill-creation-workflow.md#skill-md-template`

### Phase 3: Content Development

#### Step 5: Write Core Workflow (SKILL.md)

**Pattern:**
```markdown
## Instructions

### Phase 1: Setup
1. **Action**: What to do
   - Specific commands
2. **Validation**: Confirm it worked

### Phase 2: Implementation
1. **Action**: Main steps
   - Mini examples (< 10 lines)
   - **See:** references/examples.md#section
2. **Validation**: Check results

### Phase 3: Completion
1. **Finalize**: Complete task
2. **Document**: Record results
```

**Key principles:**
- Imperative mood ("Create" not "You should create")
- Mini examples (2-10 lines max)
- Reference detailed docs
- Target: 300-400 lines total

**See:** `references/skill-creation-workflow.md#writing-instructions`

#### Step 6: Create Reference Documentation

**Create these files as needed:**

**references/examples.md** - Complete implementations
```markdown
# Example 1: User Authentication
(Full 50-line implementation with context)

# Example 2: Dashboard
(Another complete implementation)
```

**references/quick-reference.md** - Code snippets
```markdown
## Basic Pattern
```code
(2-5 line snippet)
```

## Advanced Pattern
```code
(another snippet)
```
```

**references/troubleshooting.md** - Common errors
```markdown
## Error: "Module not found"
**Cause:** Path issue
**Solution:** Fix import path
```

**references/official-docs/** - For tech-specific skills
- Use Context7 MCP to fetch official docs
- Store in this directory
- Reference from SKILL.md

**See:** `references/documentation-guide.md` for complete patterns

#### Step 7: Add Scripts (Optional)

**When to use scripts:**
- Complex validation logic
- Data processing
- API interactions
- File generation

**Template:**
```python
#!/usr/bin/env python3
"""Script description"""
import sys, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    # Logic here

if __name__ == "__main__":
    main()
```

**Make executable:**
```bash
chmod +x scripts/script-name.py
```

**See:** `references/script-templates.md` for more examples

### Phase 4: Validation

#### Step 8: Validate Skill Structure

**Quick checklist:**
- [ ] SKILL.md < 500 lines (501 acceptable)
- [ ] Valid YAML frontmatter
- [ ] Code examples < 10 lines each
- [ ] References to detailed docs present
- [ ] Detailed content in references/
- [ ] All sections present

**Run validation (if available):**
```bash
python3 scripts/validate-skill.py --path .claude/skills/skill-name
```

**Common issues:**
```bash
# Invalid name → Use lowercase-with-hyphens
# Too long → Extract to references/
# Missing sections → Add required sections
# Vague references → Be specific: references/file.md#section
```

**See:** `references/validation-checklist.md` for complete list

#### Step 9: Test Skill

**Testing process:**
1. Restart Claude Code
2. Test with trigger keywords
3. Verify workflow executes correctly
4. Check references load properly
5. Test error handling paths

**If issues:**
1. Update SKILL.md
2. Reload Claude
3. Retest
4. Iterate

### Phase 5: Documentation

#### Step 10: Create README.md

**Template:**
```markdown
# Skill Name

Brief description.

## Installation
\`\`\`bash
cp -r skill-name .claude/skills/
\`\`\`

## Usage
"Create a [thing] with [feature]"

## Features
- Feature 1
- Feature 2
```

**See:** `references/readme-template.md`

## Common Patterns

### Pattern 1: Simple Skill (No Scripts)
- SKILL.md: Core workflow (400 lines)
- references/examples.md: Complete examples
- No scripts needed

**See:** `references/examples.md#simple-skill-pattern`

### Pattern 2: Complex Skill (With Scripts)
- SKILL.md: Workflow + script calls (450 lines)
- references/: Detailed docs
- scripts/: Automation

**See:** `references/examples.md#complex-skill-pattern`

### Pattern 3: Tech-Specific Skill
- SKILL.md: Core patterns (480 lines)
- references/official-docs/: Context7 fetched docs
- references/examples.md: Complete projects

**See:** `references/examples.md#tech-specific-pattern`

## Error Handling

| Error | Solution |
|-------|----------|
| Skill not loading | Check YAML syntax, restart Claude |
| Skill not activating | Add trigger keywords to description |
| SKILL.md too long | Extract to references/ |
| Scripts failing | Add error handling, document dependencies |
| References not found | Use correct paths: `references/file.md` |

**See:** `references/troubleshooting.md` for detailed solutions

## Decision Trees

### Should I Create a Skill?
```
Task repeated 5+ times? → Yes → Create skill
                       → No → Don't create skill

Has clear steps? → Yes → Create skill
                → No → Document workflow first

Has trigger keywords? → Yes → Create skill
                     → No → Define triggers first
```

### Where Does Content Go?
```
Core workflow steps? → SKILL.md
Complete examples? → references/examples.md
Code snippets? → references/quick-reference.md
Error solutions? → references/troubleshooting.md
Deep explanations? → references/official-docs/
Scripts needed? → scripts/
```

## Validation Checklist

**Structure:**
- [ ] Directory structure correct
- [ ] SKILL.md exists (< 500 lines)
- [ ] references/ exists with appropriate files
- [ ] README.md exists

**Content:**
- [ ] YAML frontmatter valid
- [ ] Description has trigger keywords
- [ ] Overview is brief (< 50 lines)
- [ ] Instructions are clear with phases
- [ ] Mini examples (< 10 lines each)
- [ ] References to detailed docs
- [ ] Error handling section present

**Progressive Disclosure:**
- [ ] SKILL.md under 500 lines
- [ ] Detailed examples in references/examples.md
- [ ] Snippets in references/quick-reference.md
- [ ] Troubleshooting in references/troubleshooting.md
- [ ] Clear references from SKILL.md

**See:** `references/validation-checklist.md` for complete list

## References

**Local Documentation:**
- Progressive disclosure guide: `references/progressive-disclosure-guide.md`
- Detailed workflow: `references/skill-creation-workflow.md`
- Example patterns: `references/examples.md`
- Script templates: `references/script-templates.md`
- Troubleshooting: `references/troubleshooting.md`
- Validation checklist: `references/validation-checklist.md`

**External:**
- Claude Code Docs: https://docs.claude.com
- Skills Guide: https://docs.claude.com/skills

## Tips for Success

1. **Read progressive disclosure guide first** - Critical for proper structure
2. **Start with 300 lines** - Easier to add than remove
3. **Mini examples only** - 2-10 lines max in SKILL.md
4. **Reference detailed docs** - Use clear paths
5. **Test early** - Don't wait until complete
6. **Use Context7** - For tech-specific skills
7. **Validate often** - Check line count regularly

**Real example:**
- Next.js 16 skill: 962 → 501 lines (48% improvement)
- Same information, much faster

## Version History

**v2.0.0 (2026-01-01)**
- Optimized to < 500 lines following progressive disclosure
- Added comprehensive reference documentation
- Enhanced validation checklist
- Real-world examples (Next.js 16)
- Improved pattern documentation

**v1.0.0**
- Initial release
