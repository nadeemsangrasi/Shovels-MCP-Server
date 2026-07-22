# Skill Creator Installation Guide

## Quick Installation

### Option 1: Use in Current Project

The skill is already installed at:
```
.claude/skills/skill-creator/
```

No additional installation needed! The skill will be available when you use Claude Code in this project.

### Option 2: Install Globally (Personal Skills)

To use this skill across all your projects:

```bash
# From this project directory
cp -r .claude/skills/skill-creator ~/.claude/skills/

# Or create a symlink (recommended for updates)
mkdir -p ~/.claude/skills
ln -s "$(pwd)/.claude/skills/skill-creator" ~/.claude/skills/skill-creator
```

## Verify Installation

Restart Claude Code and check if the skill is loaded:

```bash
claude --debug
# Look for "skill-creator" in the loaded skills list
```

## First Use

Try creating your first skill:

```
User: "Create a skill for generating commit messages"
```

Claude will activate the skill-creator and guide you through the process!

## Manual Script Usage

You can also use the scripts directly:

```bash
# Create skill structure
python3 .claude/skills/skill-creator/scripts/create-skill-structure.py \
  --name my-skill --location personal

# Generate template
python3 .claude/skills/skill-creator/scripts/generate-skill-template.py \
  --name my-skill \
  --description "My skill description" \
  --output ~/.claude/skills/my-skill/SKILL.md

# Validate
python3 .claude/skills/skill-creator/scripts/validate-skill.py \
  --path ~/.claude/skills/my-skill
```

## Troubleshooting

### Skill Not Loading

1. Check path: `.claude/skills/skill-creator/SKILL.md` should exist
2. Restart Claude Code
3. Try debug mode: `claude --debug`

### Scripts Not Working

```bash
# Make scripts executable
chmod +x .claude/skills/skill-creator/scripts/*.py

# Check Python version (needs 3.8+)
python3 --version
```

## Next Steps

1. Read the comprehensive documentation: `README.md`
2. Check best practices: `references/best-practices.md`
3. Review templates: `references/skill-template.md`
4. Create your first skill!

## Support

For issues or questions:
1. Check `README.md` for detailed documentation
2. Review `references/best-practices.md` for guidance
3. Run validation scripts for specific issues
