#!/usr/bin/env python3
"""
Generate SKILL.md template with proper YAML frontmatter

Usage:
    python3 generate-skill-template.py --name SKILL_NAME --description "DESCRIPTION" [options]
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


SKILL_TEMPLATE = """---
name: {name}
description: {description}
version: {version}
{allowed_tools_line}{author_line}{tags_line}---

# {title}

## Overview

{overview}

## When to Use This Skill

- When you need to {use_case_1}
- When working with {use_case_2}
- When the user mentions {use_case_3}

## Prerequisites

### Required Setup
- Claude Code installed and configured
- Required dependencies (list specific requirements here)

### Optional Dependencies
- Additional tools or packages (if any)

## Instructions

### Step 1: Preparation

1. **Gather Requirements**: What information or files are needed
2. **Validate Prerequisites**: Check that required tools/files are available
3. **Set Up Environment**: Any initial setup steps

### Step 2: Main Execution

1. **Primary Action**: Main task to perform
   ```bash
   # Example command
   command --option value
   ```

2. **Process Results**: Handle the output
   - Expected output format
   - What to do with results

### Step 3: Validation

1. **Verify Success**: Check that the task completed correctly
   - Success criteria
   - What to validate

2. **Handle Errors**: If something fails
   - Common error patterns
   - Recovery steps

### Step 4: Completion

1. **Finalize**: Complete the task
   - Any cleanup needed
   - Final steps

2. **Report**: Document results
   - What to report to user
   - Success message format

## Examples

### Example 1: Basic Usage

**Scenario**: Describe a common use case

**Input:**
```
Example input or command
```

**Process:**
1. Step one of the process
2. Step two of the process

**Output:**
```
Expected output or result
```

### Example 2: Advanced Usage

**Scenario**: Describe a more complex use case

**Input:**
```
Example input for advanced scenario
```

**Process:**
1. Advanced step one
2. Advanced step two

**Output:**
```
Expected advanced output
```

## Error Handling

### Error: Common Issue 1

```
Error message example
```

**Solution:**
1. Diagnostic step
2. Fix action
3. Verification

### Error: Common Issue 2

```
Another error message
```

**Solution:**
1. How to identify the issue
2. Steps to resolve
3. How to prevent in future

## Limitations

### What This Skill Cannot Do

- Limitation 1: Explain what's out of scope
- Limitation 2: Specific constraints
- Limitation 3: Known edge cases

### Known Constraints

- Constraint 1: Technical limitation
- Constraint 2: Environmental requirement
- Constraint 3: Dependency limitation

## Validation Checklist

Before completing the task, verify:

- [ ] Requirement 1 met
- [ ] Requirement 2 met
- [ ] Requirement 3 met
- [ ] Output validated
- [ ] No errors present

## References

### Internal Files
- Related documentation: `references/guide.md` (if applicable)
- Additional examples: `references/examples.md` (if applicable)

### External Resources
- Official documentation: [Link if applicable]
- Related tools: [Link if applicable]

## Tips for Success

### Best Practice 1
Explain a key best practice for using this skill effectively

### Best Practice 2
Another important tip for optimal results

### Best Practice 3
Additional guidance for success

## Version History

### v{version} ({date})
- Initial release
- Core functionality implemented
"""


def validate_name(name):
    """Validate skill name"""
    if len(name) > 64:
        return False, "Name must be 64 characters or less"
    if not name.islower():
        return False, "Name must be lowercase"
    for char in name:
        if not (char.isalnum() or char == '-'):
            return False, "Name can only contain lowercase letters, numbers, and hyphens"
    return True, "Valid"


def validate_description(description):
    """Validate description"""
    if len(description) > 1024:
        return False, f"Description must be 1024 characters or less (currently {len(description)})"
    if '<' in description or '>' in description:
        return False, "Description cannot contain XML tags"
    if not description.strip():
        return False, "Description cannot be empty"
    return True, "Valid"


def generate_template(args):
    """Generate SKILL.md from template"""

    # Validate inputs
    is_valid, message = validate_name(args.name)
    if not is_valid:
        print(f"Error: Invalid name - {message}", file=sys.stderr)
        return False

    is_valid, message = validate_description(args.description)
    if not is_valid:
        print(f"Error: Invalid description - {message}", file=sys.stderr)
        return False

    # Prepare template variables
    title = args.name.replace('-', ' ').title()

    # Build optional YAML lines
    allowed_tools_line = ""
    if args.allowed_tools:
        allowed_tools_line = f"allowed-tools: {args.allowed_tools}\n"

    author_line = ""
    if args.author:
        author_line = f"author: {args.author}\n"

    tags_line = ""
    if args.tags:
        tags_list = [f'"{tag.strip()}"' for tag in args.tags.split(',')]
        tags_line = f"tags: [{', '.join(tags_list)}]\n"

    # Generate overview from description (first sentence)
    overview = args.description.split('.')[0] + '.'

    # Generate use cases from description keywords
    use_case_1 = "accomplish the task described above"
    use_case_2 = "the functionality mentioned in the description"
    use_case_3 = f"'{args.name.replace('-', ' ')}'"

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Fill template
    content = SKILL_TEMPLATE.format(
        name=args.name,
        description=args.description,
        version=args.version,
        allowed_tools_line=allowed_tools_line,
        author_line=author_line,
        tags_line=tags_line,
        title=title,
        overview=overview,
        use_case_1=use_case_1,
        use_case_2=use_case_2,
        use_case_3=use_case_3,
        date=current_date
    )

    # Write to output file
    try:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        print(f"✓ Generated SKILL.md: {output_path}")
        print(f"\nNext steps:")
        print(f"1. Edit {output_path} to customize instructions")
        print(f"2. Replace placeholder use cases with specific triggers")
        print(f"3. Add concrete examples with real inputs/outputs")
        print(f"4. Fill in error handling scenarios")
        print(f"5. Validate: python3 scripts/validate-skill.py --path {output_path.parent}")
        return True

    except Exception as e:
        print(f"Error writing template: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate SKILL.md template with proper YAML frontmatter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Minimal skill
    python3 generate-skill-template.py \\
        --name "commit-messages" \\
        --description "Generate semantic commit messages from git diffs" \\
        --output ~/.claude/skills/commit-messages/SKILL.md

    # Complete skill with all options
    python3 generate-skill-template.py \\
        --name "api-tester" \\
        --description "Test REST APIs with validation" \\
        --version "2.0.0" \\
        --allowed-tools "Bash, Read, Write" \\
        --author "Your Name" \\
        --tags "api, testing, automation" \\
        --output ~/.claude/skills/api-tester/SKILL.md
        """
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Skill name (lowercase, hyphens only, max 64 chars)"
    )

    parser.add_argument(
        "--description",
        required=True,
        help="Skill description (max 1024 chars, include trigger keywords)"
    )

    parser.add_argument(
        "--version",
        default="1.0.0",
        help="Skill version (semantic versioning, default: 1.0.0)"
    )

    parser.add_argument(
        "--allowed-tools",
        help="Comma-separated list of allowed tools (e.g., 'Bash, Read, Write')"
    )

    parser.add_argument(
        "--author",
        help="Skill author name"
    )

    parser.add_argument(
        "--tags",
        help="Comma-separated tags (e.g., 'api, testing, automation')"
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output file path (e.g., ~/.claude/skills/skill-name/SKILL.md)"
    )

    args = parser.parse_args()

    success = generate_template(args)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
