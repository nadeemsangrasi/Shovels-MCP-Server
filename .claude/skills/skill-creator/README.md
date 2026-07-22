# Skill Creator - Claude Code Skill

A comprehensive skill for creating new Claude Code skills with proper structure, validation, and best practices.

## Overview

The Skill Creator skill automates and guides the process of building new Claude Code skills. It provides:

- Automated directory structure creation
- SKILL.md template generation with validated YAML frontmatter
- Supporting script templates
- Reference documentation
- Comprehensive validation tools
- Best practices guidance

## Installation

### Personal Skills (Available Across All Projects)

```bash
# Copy to personal skills directory
cp -r skill-creator ~/.claude/skills/

# Or symlink if you want to keep it updated
ln -s "$(pwd)/skill-creator" ~/.claude/skills/skill-creator
```

### Project Skills (Specific to This Project)

```bash
# Copy to project skills directory
mkdir -p .claude/skills
cp -r skill-creator .claude/skills/

# Commit to version control for team use
git add .claude/skills/skill-creator
git commit -m "Add skill-creator skill for team"
```

## Prerequisites

### Required
- Claude Code installed and configured
- Python 3.8 or higher
- Bash shell (for script execution)

### Optional
- PyYAML for advanced validation (`pip install pyyaml`)
- Git for version control
- Context7 MCP server for fetching official documentation of technologies

## Usage

### Quick Start

**Activate the skill by saying:**

```
"Create a skill for [your use case]"
"Help me build a Claude skill for [task]"
"Generate a new skill called [name]"
```

**Example:**
```
User: "Create a skill for generating API documentation from code"

Claude will:
1. Gather requirements (name, description, triggers)
2. Create directory structure
3. Generate SKILL.md template
4. Guide you through customization
5. Validate the result
```

### Manual Workflow

If you prefer to use the scripts directly:

#### 1. Create Structure

```bash
python3 ~/.claude/skills/skill-creator/scripts/create-skill-structure.py \
  --name "your-skill-name" \
  --location personal
```

#### 2. Generate SKILL.md

```bash
python3 ~/.claude/skills/skill-creator/scripts/generate-skill-template.py \
  --name "your-skill-name" \
  --description "Your skill description with trigger keywords" \
  --allowed-tools "Bash, Read, Write" \
  --output ~/.claude/skills/your-skill-name/SKILL.md
```

#### 3. Customize Content

Edit the generated SKILL.md:
- Replace placeholder use cases
- Add concrete examples
- Document error handling
- Fill in validation checklists

#### 4. Validate

```bash
python3 ~/.claude/skills/skill-creator/scripts/validate-skill.py \
  --path ~/.claude/skills/your-skill-name \
  --verbose
```

#### 5. Test

```bash
# Restart Claude Code to load new skill
claude

# Test activation
# Try: "Use the [your-skill-name] skill to [task]"
```

## Features

### Automated Structure Creation
- Creates proper directory hierarchy (scripts/, references/, assets/)
- Sets up placeholder files
- Validates naming conventions

### Template Generation
- Complete SKILL.md with all recommended sections
- Valid YAML frontmatter
- Standard section structure
- Placeholder content you customize

### Validation Tools
- YAML syntax validation
- Frontmatter field validation
- Content structure checking
- Script executable verification
- Reference file existence checks

### Best Practices Integration
- Progressive disclosure guidance
- Description writing tips
- Instruction clarity patterns
- Error handling templates
- Testing strategies

## Directory Structure

```
skill-creator/
├── SKILL.md                          # Main skill instructions
├── scripts/                          # Automation tools
│   ├── create-skill-structure.py    # Directory setup
│   ├── generate-skill-template.py   # SKILL.md generation
│   ├── validate-skill.py            # Comprehensive validation
│   └── validate-yaml.py             # YAML syntax checker
├── references/                       # Supporting documentation
│   ├── skill-template.md            # Complete template reference
│   ├── best-practices.md            # Best practices guide
│   └── yaml-schema.json             # Frontmatter schema
└── README.md                         # This file
```

## Examples

### Example 1: Simple Skill (No Scripts)

Create a commit message generator:

```bash
# 1. Create structure
python3 scripts/create-skill-structure.py \
  --name "commit-messages" \
  --location personal

# 2. Generate template
python3 scripts/generate-skill-template.py \
  --name "commit-messages" \
  --description "Generate semantic commit messages from git diffs" \
  --allowed-tools "Bash, Read" \
  --output ~/.claude/skills/commit-messages/SKILL.md

# 3. Edit SKILL.md to add git workflow instructions

# 4. Validate
python3 scripts/validate-skill.py --path ~/.claude/skills/commit-messages
```

### Example 2: Complex Skill (With Scripts)

Create an API testing skill:

```bash
# 1. Create structure
python3 scripts/create-skill-structure.py \
  --name "api-tester" \
  --location personal

# 2. Generate template
python3 scripts/generate-skill-template.py \
  --name "api-tester" \
  --description "Test REST APIs with validation" \
  --version "1.0.0" \
  --allowed-tools "Bash, Read, Write" \
  --author "Your Name" \
  --tags "api, testing, automation" \
  --output ~/.claude/skills/api-tester/SKILL.md

# 3. Add scripts
cat > ~/.claude/skills/api-tester/scripts/test-endpoint.py << 'EOF'
#!/usr/bin/env python3
# Your test script here
EOF
chmod +x ~/.claude/skills/api-tester/scripts/test-endpoint.py

# 4. Add references
cat > ~/.claude/skills/api-tester/references/api-spec.yaml << 'EOF'
# OpenAPI spec example
EOF

# 5. Edit SKILL.md to reference scripts

# 6. Validate
python3 scripts/validate-skill.py --path ~/.claude/skills/api-tester --verbose
```

## Configuration

### Skill Locations

**Personal Skills:** `~/.claude/skills/`
- Available in all projects
- User-specific preferences

**Project Skills:** `.claude/skills/` (in project root)
- Available only in this project
- Shared with team via git

### Using Context7 MCP for Documentation

When creating skills for specific technologies, leverage Context7 to fetch official documentation:

**Supported Use Cases:**
- Frameworks: React, Vue, Django, FastAPI, Express, etc.
- Libraries: pytest, requests, pandas, numpy, etc.
- APIs: GitHub, Stripe, AWS, Google Cloud, etc.
- Languages: Python, JavaScript, Go, Rust patterns

**Workflow:**
1. **Request Documentation**
   ```
   "Use Context7 to fetch FastAPI official documentation"
   "Get React Testing Library docs via Context7"
   ```

2. **Save to References**
   - Claude saves fetched docs to `references/official-docs/`
   - Keeps documentation with the skill for offline access

3. **Reference in SKILL.md**
   ```markdown
   ## Prerequisites
   ### Framework Documentation
   - FastAPI: `references/official-docs/fastapi-guide.md`
   ```

**Benefits:**
- Always use official, up-to-date documentation
- Ensure accuracy and best practices
- Provide comprehensive references
- Enable offline development

### Allowed Tools

Control which tools Claude can use during skill execution:

```yaml
allowed-tools: Bash, Read, Write  # Full access
allowed-tools: Read, Grep, Glob   # Read-only
allowed-tools: Read               # Maximum security
```

## Troubleshooting

### Skill Not Loading

**Symptoms:** Skill doesn't appear in Claude's loaded skills

**Solutions:**
1. Check file location: must be in `.claude/skills/[name]/SKILL.md`
2. Validate YAML: `python3 scripts/validate-yaml.py --file SKILL.md`
3. Check permissions: file must be readable
4. Restart Claude Code

### Validation Errors

**Invalid YAML Syntax:**
```bash
python3 scripts/validate-yaml.py --file path/to/SKILL.md
```

**Frontmatter Issues:**
```bash
python3 scripts/validate-skill.py --path path/to/skill --verbose
```

### Scripts Not Executable

```bash
# Make scripts executable
chmod +x scripts/*.py scripts/*.sh

# Verify
ls -la scripts/
# Should show -rwxr-xr-x permissions
```

## Contributing

### Reporting Issues

If you find bugs or have suggestions:

1. Check existing issues
2. Create detailed bug report with:
   - What you tried to do
   - What happened
   - What you expected
   - Steps to reproduce

### Submitting Improvements

1. Fork/branch
2. Make changes
3. Test thoroughly
4. Update documentation
5. Submit pull request

## Version History

### v1.0.0 (2026-01-01)
- Initial release
- Core skill creation workflow
- Validation scripts
- Template generation
- Best practices integration
- Comprehensive documentation

## License

MIT License - See LICENSE file for details

## Resources

### Internal Documentation
- Complete template: `references/skill-template.md`
- Best practices: `references/best-practices.md`
- YAML schema: `references/yaml-schema.json`

### External Links
- [Claude Code Documentation](https://docs.claude.com)
- [Skills Guide](https://docs.claude.com/skills)
- [Example Skills](https://github.com/anthropics/claude-skills)

## Support

For help with skill creation:

1. Use the skill: "Help me create a skill for [your use case]"
2. Read documentation in `references/`
3. Check validation output for specific issues
4. Review examples in this README

## Tips for Success

1. **Start Simple**: Create minimal skill first, add complexity later
2. **Test Early**: Validate and test after each major change
3. **Use Templates**: Don't write from scratch, use provided templates
4. **Be Specific**: Clear descriptions with trigger keywords
5. **Iterate**: Get feedback and refine based on real usage

---

**Created with:** Skill Creator v1.0.0
**Maintained by:** SpecKit Plus
**Last Updated:** 2026-01-01
