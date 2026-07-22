# Skill Creation Best Practices

This document compiles best practices for creating effective Claude Code skills based on official guidelines and real-world experience.

## Table of Contents

1. [Description Writing](#description-writing)
2. [Instruction Clarity](#instruction-clarity)
3. [Progressive Disclosure](#progressive-disclosure)
4. [Script Design](#script-design)
5. [Using Context7 for Documentation](#using-context7-for-documentation)
6. [Error Handling](#error-handling)
7. [Testing Strategy](#testing-strategy)
8. [Maintenance](#maintenance)

---

## Description Writing

The description is **critical** for skill discovery. Claude uses it to determine when to invoke your skill.

### Key Principles

**1. Be Specific and Action-Oriented**

❌ Bad: "Helps with PDFs"
✓ Good: "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

**2. Include Trigger Keywords**

Think about what users would actually say:
- "Use when working with [specific technology]"
- "Use when the user mentions [keywords]"
- "Use for [specific tasks]"

**3. Use Action Verbs**

Start with strong verbs:
- Extract, create, analyze, validate, generate, process, convert, review, test, deploy, document, optimize

**4. Keep It Concise**

- Target: 100-200 characters
- Maximum: 1024 characters
- Focus on: What + When

### Template

```
[Action verb] [what] [how/with what]. Use when [trigger condition 1], [condition 2], or when user mentions [keywords].
```

### Examples

**API Testing:**
```yaml
description: Test REST APIs with automated validation of status codes, response structure, and data types. Use for API testing, integration verification, or debugging endpoints.
```

**Commit Messages:**
```yaml
description: Generate semantic commit messages from git diffs following Conventional Commits. Use when writing commit messages or staging changes.
```

**Code Review:**
```yaml
description: Review code changes following team standards for style, security, performance, and testing. Use when reviewing pull requests or code commits.
```

---

## Instruction Clarity

Instructions must be clear enough for Claude to follow autonomously.

### Writing Style

**Use Imperative Mood**

❌ "You should read the file"
❌ "The file needs to be read"
✓ "Read the file"

**Be Concrete, Not Abstract**

❌ "Process the data appropriately"
✓ "Parse the JSON response and extract the 'user' field"

**Show, Don't Tell**

Include actual commands:
```markdown
### Step 1: Check Status

Run the status command:
```bash
git status --short
```

Expected output:
```
M  src/main.py
?? new-file.txt
```
```

### Structure Pattern

```markdown
## Instructions

### Phase 1: Preparation
1. **Action**: What to do
   - Specific detail
   - Expected result
2. **Verification**: How to confirm
   - What to check
   - Success criteria

### Phase 2: Execution
1. **Main Task**: Primary action
   - Command or tool use
   - Output handling
2. **Process**: Handle results
   - Next steps
   - Conditional logic

### Phase 3: Validation
1. **Verify**: Check success
   - Validation points
   - Error detection
2. **Handle**: Address issues
   - Error recovery
   - Fallback options

### Phase 4: Completion
1. **Finalize**: Complete task
   - Cleanup
   - Final steps
2. **Document**: Record results
   - What to report
   - Success message
```

### Numbered vs Bulleted Lists

**Use Numbered Lists When:**
- Steps must be sequential
- Order matters
- Steps build on each other

**Use Bullet Points When:**
- Options are available
- Order doesn't matter
- Listing attributes or features

### Code Block Best Practices

**Always Include:**
1. Language identifier: ```bash, ```python, ```json
2. Comments explaining non-obvious parts
3. Expected output when relevant

**Example:**
````markdown
Run the validation script:

```bash
python3 scripts/validate.py --input data.json --strict
```

Expected output:
```
✓ Schema validation passed
✓ All required fields present
✓ Data types correct
```

If validation fails:
```
✗ Validation failed: Missing required field 'email'
```
````

---

## Progressive Disclosure

Keep SKILL.md focused; delegate details to other files.

### What Belongs Where

**SKILL.md (Core, <500 lines):**
- Overview and purpose
- When to use triggers
- Step-by-step instructions
- Basic examples
- Common errors
- References to other files

**references/ (Detailed, unlimited):**
- Complete API documentation
- Extended examples
- Troubleshooting guides
- Configuration options
- Background information

**scripts/ (Automation):**
- Data processing
- Validation logic
- Complex calculations
- API interactions
- Report generation

**assets/ (Resources):**
- Templates
- Images
- Binary files
- Configuration files

### Reference Pattern

In SKILL.md:
```markdown
## Database Schema

For complete schema documentation, see `references/database-schema.md`

Key tables:
- users: User account information
- posts: User-generated content
- comments: Post comments

Query the schema using:
```bash
python3 scripts/query-db.py --schema
```
```

In references/database-schema.md:
```markdown
# Complete Database Schema

## Users Table
- id: INTEGER PRIMARY KEY
- email: VARCHAR(255) UNIQUE NOT NULL
- password_hash: VARCHAR(255) NOT NULL
- created_at: TIMESTAMP DEFAULT NOW()
... (detailed documentation)
```

---

## Script Design

Scripts make skills more reliable by delegating complex operations to tested code.

### When to Use Scripts

**Good Use Cases:**
- Data transformations (parsing, formatting)
- Complex calculations
- API interactions
- Validation logic
- File processing
- Report generation

**Bad Use Cases:**
- Simple file reads (use Read tool)
- Basic commands (use Bash tool directly)
- One-liner operations

### Script Template

```python
#!/usr/bin/env python3
"""
Brief description of what this script does

Usage:
    python3 script-name.py --input FILE --output FILE [--option VALUE]

Examples:
    python3 script-name.py --input data.json --output report.html
    python3 script-name.py --input data.json --format text --verbose
"""

import sys
import argparse
import json
from pathlib import Path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Script purpose",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Required arguments
    parser.add_argument(
        "--input",
        required=True,
        help="Input file path"
    )

    # Optional arguments
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)"
    )

    parser.add_argument(
        "--format",
        choices=["json", "text", "html"],
        default="json",
        help="Output format (default: json)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    try:
        # Validate input
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Process
        if args.verbose:
            print(f"Processing {args.input}...", file=sys.stderr)

        result = process_input(input_path, args.format)

        # Output
        if args.output:
            Path(args.output).write_text(result)
            if args.verbose:
                print(f"✓ Written to {args.output}", file=sys.stderr)
        else:
            print(result)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def process_input(input_path, format_type):
    """Process input file and return formatted result"""
    # Read input
    data = json.loads(input_path.read_text())

    # Process
    result = transform_data(data)

    # Format
    if format_type == "json":
        return json.dumps(result, indent=2)
    elif format_type == "text":
        return format_as_text(result)
    elif format_type == "html":
        return format_as_html(result)


def transform_data(data):
    """Transform input data"""
    # Implementation here
    return data


def format_as_text(data):
    """Format data as plain text"""
    return str(data)


def format_as_html(data):
    """Format data as HTML"""
    return f"<html><body>{data}</body></html>"


if __name__ == "__main__":
    main()
```

### Script Best Practices

1. **Include Shebang**: `#!/usr/bin/env python3`
2. **Add Docstring**: Usage and examples
3. **Use argparse**: Clear argument handling
4. **Validate Input**: Check files exist, types correct
5. **Handle Errors**: Try/except with clear messages
6. **Exit Codes**: 0 for success, 1+ for errors
7. **Verbose Mode**: Optional detailed output
8. **Help Text**: Clear descriptions for all arguments

### Referencing Scripts in SKILL.md

````markdown
### Validation Step

Run the validation script to check data integrity:

```bash
python3 scripts/validate.py --input data.json --strict
```

**Arguments:**
- `--input`: Path to JSON data file (required)
- `--strict`: Enable strict validation (optional)
- `--verbose`: Show detailed output (optional)

**Output:**

Success:
```
✓ Schema validation passed
✓ All required fields present (10/10)
✓ Data types correct
```

Failure:
```
✗ Validation failed
  - Missing required field: 'email'
  - Invalid type for 'age': expected integer, got string
```

**Exit Codes:**
- 0: Validation passed
- 1: Validation failed
- 2: Invalid arguments
````

---

## Using Context7 for Documentation

When creating skills for specific technologies, frameworks, or APIs, use Context7 MCP to fetch official documentation.

### When to Use Context7

**Good Use Cases:**
- Framework-specific skills (React, Django, FastAPI, Vue, etc.)
- Library integration skills (pytest, pandas, requests, etc.)
- API interaction skills (GitHub API, Stripe, AWS, etc.)
- Language pattern skills (Python async, JavaScript promises, Go concurrency)
- Tool-specific workflows (Docker, Kubernetes, Terraform)

**Not Needed For:**
- Generic workflows (git commits, file organization)
- Internal company processes
- Simple utility tasks
- Language-agnostic patterns

### How to Use Context7

#### Step 1: Identify Documentation Needs

Before creating the skill, list what official documentation would help:

```markdown
Skill: react-testing
Documentation needed:
- React Testing Library API reference
- Jest configuration guide
- React hooks testing patterns
- Common testing scenarios
```

#### Step 2: Fetch Documentation

Use Context7 to retrieve official docs:

```
User: "Use Context7 to fetch React Testing Library documentation"
User: "Get Jest configuration guide via Context7"
User: "Fetch React hooks testing patterns using Context7"
```

Claude will retrieve and save the documentation.

#### Step 3: Organize Documentation

Create a clear structure in `references/`:

```
skill-name/references/
├── official-docs/              # Raw docs from Context7
│   ├── main-framework.md       # Primary framework guide
│   ├── api-reference.md        # Complete API documentation
│   └── best-practices.md       # Official recommendations
├── summaries/                  # Your condensed versions
│   ├── quick-start.md          # Essential setup steps
│   └── common-patterns.md      # Frequently used patterns
└── examples/                   # Practical examples
    ├── basic-usage.md
    └── advanced-scenarios.md
```

#### Step 4: Reference in SKILL.md

Make documentation easily accessible:

```markdown
## Prerequisites

### Official Documentation
- React Testing Library: `references/official-docs/react-testing-library.md`
- Jest Configuration: `references/official-docs/jest-config.md`
- Testing Patterns: `references/official-docs/testing-patterns.md`

### Quick References
- Common patterns: `references/summaries/common-patterns.md`
- Quick start: `references/summaries/quick-start.md`

## Instructions

### Step 1: Setup Testing Environment

Follow the official Jest setup guide: `references/official-docs/jest-config.md`

Key configuration points:
1. Install dependencies (see documentation)
2. Create jest.config.js as specified
3. Add test scripts to package.json
```

### Best Practices for Context7 Documentation

#### 1. Fetch Early in Skill Creation

Get documentation before writing instructions:

```
Workflow:
1. Create skill structure
2. Fetch Context7 documentation ← Do this early
3. Review fetched docs
4. Write SKILL.md instructions based on official patterns
5. Reference docs in SKILL.md
```

#### 2. Organize by Purpose

Separate different types of documentation:

```
references/
├── official-docs/          # Complete references (use when needed)
│   ├── full-guide.md
│   └── complete-api.md
├── quick-refs/            # Condensed for quick lookup
│   └── cheat-sheet.md
└── examples/              # Practical applications
    └── cookbook.md
```

#### 3. Create Summaries

Don't just store raw docs—create usable summaries:

**In `references/summaries/quick-start.md`:**
```markdown
# FastAPI Quick Start (from official docs)

## Installation
```bash
pip install fastapi uvicorn
```

## Basic App Structure
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

## Running
```bash
uvicorn main:app --reload
```

For complete documentation, see `../official-docs/fastapi-guide.md`
```

#### 4. Keep Documentation Updated

Add notes about documentation freshness:

```markdown
## References

### Official Documentation
- FastAPI Guide: `references/official-docs/fastapi-guide.md`
  - Fetched: 2026-01-01
  - Version: FastAPI 0.104.0
  - Update: Re-fetch if using newer versions
```

### Example: Creating a FastAPI Skill with Context7

**Complete Workflow:**

```bash
# 1. Create structure
python3 scripts/create-skill-structure.py \
  --name "fastapi-developer" \
  --location personal

# 2. Fetch documentation
# User: "Use Context7 to fetch FastAPI official documentation"
# User: "Get Pydantic models documentation via Context7"
# User: "Fetch SQLAlchemy async patterns using Context7"

# Result:
# - references/official-docs/fastapi-guide.md
# - references/official-docs/pydantic-models.md
# - references/official-docs/sqlalchemy-async.md

# 3. Create summaries
cat > references/summaries/fastapi-quick-ref.md << 'EOF'
# FastAPI Quick Reference

## Project Setup
[Essential steps from official docs]

## Common Patterns
[Frequently used patterns]

## Troubleshooting
[Common issues and solutions]

See complete guide: `../official-docs/fastapi-guide.md`
EOF

# 4. Generate SKILL.md and reference docs
python3 scripts/generate-skill-template.py \
  --name "fastapi-developer" \
  --description "Build FastAPI applications following official best practices" \
  --output fastapi-developer/SKILL.md

# 5. Edit SKILL.md to include doc references
```

**In SKILL.md:**
```markdown
## Prerequisites

### Framework Documentation
- FastAPI Complete Guide: `references/official-docs/fastapi-guide.md`
- Pydantic Models: `references/official-docs/pydantic-models.md`
- SQLAlchemy Async: `references/official-docs/sqlalchemy-async.md`
- Quick Reference: `references/summaries/fastapi-quick-ref.md`

## Instructions

### Step 1: Project Setup

Follow the official setup guide: `references/official-docs/fastapi-guide.md`

Key steps:
1. Install FastAPI and Uvicorn
2. Create project structure
3. Set up database connection (see `references/official-docs/sqlalchemy-async.md`)

### Step 2: Define Models

Use Pydantic for data validation: `references/official-docs/pydantic-models.md`

Example from official docs:
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
```
```

### Benefits of Using Context7

**For Skill Creators:**
- Ensures accuracy with official sources
- Saves research time
- Provides comprehensive references
- Follows framework best practices
- Keeps skills maintainable

**For Skill Users:**
- Trustworthy information
- Official patterns and conventions
- Up-to-date best practices
- Complete reference materials
- Offline documentation access

### Common Patterns

#### Pattern 1: Framework Skill

```
Skill: django-rest-api
Context7 Docs:
- Django REST framework guide
- Django ORM reference
- Authentication patterns

Organization:
references/official-docs/
├── drf-guide.md
├── django-orm.md
└── auth-patterns.md
```

#### Pattern 2: Library Integration Skill

```
Skill: pytest-testing
Context7 Docs:
- pytest documentation
- pytest fixtures
- pytest plugins

Organization:
references/official-docs/
├── pytest-guide.md
├── fixtures-reference.md
└── plugins-catalog.md
```

#### Pattern 3: API Integration Skill

```
Skill: github-automation
Context7 Docs:
- GitHub REST API
- GitHub Actions workflow
- GitHub CLI reference

Organization:
references/official-docs/
├── github-rest-api.md
├── actions-workflow.md
└── gh-cli-reference.md
```

### Documentation Maintenance

Keep documentation fresh:

```markdown
## Maintenance Checklist

### Quarterly Review
- [ ] Check if framework has major updates
- [ ] Re-fetch documentation if versions changed
- [ ] Update version notes in references
- [ ] Test skill with latest framework version
- [ ] Update examples if APIs changed

### When to Re-fetch
- Major framework version updates
- Significant API changes
- Deprecation warnings in your skill
- User reports of outdated information
```

---

## Error Handling

Comprehensive error handling makes skills robust and user-friendly.

### Error Documentation Template

```markdown
### Error: [Descriptive Error Name]

```
Actual error message or symptom
```

**Cause:** Why this error occurs

**Solution:**
1. Diagnostic step (how to confirm this is the issue)
2. Fix action (concrete steps to resolve)
3. Verification (how to confirm it's fixed)

**Prevention:** How to avoid this error in future
```

### Common Error Categories

**1. File Not Found**
```markdown
### Error: Input File Not Found

```
Error: Could not read file 'data.json': No such file or directory
```

**Cause:** The specified file path doesn't exist or is incorrect

**Solution:**
1. Verify the file path: `ls -la data.json`
2. Check current directory: `pwd`
3. Use absolute path or correct relative path
4. Retry with correct path

**Prevention:** Always verify file paths before running commands
```

**2. Permission Denied**
```markdown
### Error: Permission Denied

```
bash: ./script.py: Permission denied
```

**Cause:** Script is not executable

**Solution:**
1. Make script executable: `chmod +x script.py`
2. Retry execution
3. Verify: `ls -la script.py` should show `-rwxr-xr-x`

**Prevention:** Run `chmod +x` on all scripts after creating them
```

**3. Missing Dependencies**
```markdown
### Error: Module Not Found

```
ModuleNotFoundError: No module named 'requests'
```

**Cause:** Required Python package is not installed

**Solution:**
1. Install package: `pip install requests`
2. Or install all requirements: `pip install -r requirements.txt`
3. Retry the operation

**Prevention:** Document all dependencies in Prerequisites section
```

---

## Testing Strategy

Thorough testing ensures skills work reliably.

### Testing Checklist

**Phase 1: Structure Testing**
- [ ] Skill directory created correctly
- [ ] SKILL.md exists and is readable
- [ ] All referenced files exist
- [ ] Scripts are executable

**Phase 2: Loading Testing**
- [ ] Skill loads without errors (`claude --debug`)
- [ ] Appears in loaded skills list
- [ ] No YAML parsing errors
- [ ] Frontmatter validated

**Phase 3: Activation Testing**
- [ ] Explicit activation works ("Use the X skill to...")
- [ ] Implicit activation works (trigger keywords)
- [ ] Activates in appropriate contexts
- [ ] Doesn't activate inappropriately

**Phase 4: Execution Testing**
- [ ] Instructions are followable
- [ ] Commands execute successfully
- [ ] Scripts work as documented
- [ ] Error paths are handled

**Phase 5: Output Testing**
- [ ] Output format matches expectations
- [ ] Quality meets requirements
- [ ] Edge cases handled
- [ ] Errors reported clearly

### Testing Methods

**1. Debug Mode Testing**
```bash
claude --debug
# Observe:
# - Skills loaded at startup
# - Which skill activates
# - File reads
# - Script executions
# - Errors
```

**2. Explicit Testing**
```
User: "Use the [skill-name] skill to [task]"
# Forces activation for testing
```

**3. Implicit Testing**
```
User: "[natural language with trigger keywords]"
# Tests if description triggers correctly
```

**4. Two-Agent Testing**

Agent A (Creator):
- Creates/refines the skill
- Makes changes based on feedback

Agent B (Tester):
- Uses skill on real tasks
- Acts as end user would

Feedback Loop:
1. Agent A creates skill
2. Agent B tests with real tasks
3. Observe Agent B's behavior
4. Identify issues
5. Agent A refines
6. Repeat until smooth

### Common Test Failures

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Skill not loading | Invalid YAML | Validate with `scripts/validate-yaml.py` |
| Skill not activating | Poor description | Add trigger keywords users would say |
| Scripts failing | Missing dependencies | Document in Prerequisites |
| Instructions unclear | Too vague | Add concrete examples and commands |
| Wrong skill activates | Description too broad | Make more specific to use case |
| Multiple re-reads | Inefficient structure | Add summary to SKILL.md header |

---

## Maintenance

### Versioning

Use semantic versioning: MAJOR.MINOR.PATCH

**MAJOR (1.0.0 → 2.0.0):**
- Breaking changes
- Incompatible changes to interface
- Renamed fields or commands

**MINOR (1.0.0 → 1.1.0):**
- New features
- New optional parameters
- Additional functionality

**PATCH (1.0.0 → 1.0.1):**
- Bug fixes
- Documentation updates
- Performance improvements

### Changelog

Maintain a CHANGELOG.md:

```markdown
# Changelog

## [2.1.0] - 2026-01-15

### Added
- New validation step for edge cases
- Support for JSON output format
- Verbose mode for debugging

### Changed
- Improved error messages
- Updated examples with real-world scenarios
- Refactored validation logic for clarity

### Fixed
- Script execution on Windows
- Path handling for nested directories
- Edge case in data parsing

### Deprecated
- Old `--format` flag (use `--output-format` instead)

## [2.0.0] - 2026-01-01

### Breaking Changes
- Renamed `tools` to `allowed-tools` in frontmatter
- Changed script interface: now uses `--input` instead of positional arg

### Added
- Multi-language support
- Advanced filtering options

### Migration Guide
1. Update frontmatter: `tools:` → `allowed-tools:`
2. Update script calls: `script.py file.txt` → `script.py --input file.txt`
```

### Update Process

1. **Make Changes**
   - Edit SKILL.md, scripts, or references
   - Test thoroughly

2. **Update Version**
   - Increment version in frontmatter
   - Follow semantic versioning

3. **Document Changes**
   - Add entry to CHANGELOG.md
   - Include migration notes if breaking

4. **Test Across Models**
   - Test with Haiku (needs more guidance)
   - Test with Sonnet (balanced)
   - Test with Opus (handles complexity)

5. **Distribute Updates**
   - Commit changes
   - Tag release: `git tag v2.1.0`
   - Update documentation
   - Notify users if shared

### Monitoring

Track these metrics:
- Activation success rate
- Error frequency
- User feedback
- Performance (execution time)
- Usage patterns

### Iterative Improvement

Regular review cycle:
1. **Collect Feedback** (weekly/monthly)
   - What worked well?
   - What was confusing?
   - What errors occurred?

2. **Identify Patterns** (monthly)
   - Common activation failures
   - Frequent errors
   - Unclear instructions

3. **Plan Updates** (quarterly)
   - Priority fixes
   - Enhancement opportunities
   - Breaking changes needed

4. **Release** (as needed)
   - Batch related changes
   - Maintain backward compatibility when possible
   - Communicate changes clearly

---

## Quick Reference

### Pre-Creation Checklist
- [ ] Task repeated 5+ times?
- [ ] Clear, sequential steps?
- [ ] Specific trigger keywords identified?
- [ ] Scripts would improve reliability?

### Creation Checklist
- [ ] Valid name (lowercase, hyphens, ≤64 chars)
- [ ] Clear description (≤1024 chars, trigger keywords)
- [ ] Overview section complete
- [ ] When to Use section specific
- [ ] Instructions with examples
- [ ] Error handling documented
- [ ] Examples concrete and realistic

### Testing Checklist
- [ ] Loads without errors
- [ ] Activates correctly
- [ ] Instructions followable
- [ ] Scripts execute
- [ ] Errors handled gracefully

### Distribution Checklist
- [ ] README.md written
- [ ] LICENSE file included
- [ ] Installation instructions clear
- [ ] Prerequisites documented
- [ ] Version tagged

---

## Resources

### Validation Tools
- Structure validator: `scripts/validate-skill.py`
- YAML checker: `scripts/validate-yaml.py`
- Template generator: `scripts/generate-skill-template.py`

### Templates
- Complete template: `references/skill-template.md`
- Minimal template: For simple skills
- Script template: For automation-heavy skills

### External Links
- Claude Code Documentation: https://docs.claude.com
- Skills Guide: https://docs.claude.com/skills
- Community Examples: https://github.com/anthropics/claude-skills
