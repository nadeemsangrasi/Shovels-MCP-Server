#!/usr/bin/env python3
"""
Create Claude Code skill directory structure

Usage:
    python3 create-skill-structure.py --name SKILL_NAME [--location personal|project]
"""

import sys
import os
import argparse
from pathlib import Path


def validate_skill_name(name):
    """Validate skill name follows Claude Code requirements"""
    if len(name) > 64:
        return False, "Skill name must be 64 characters or less"

    if not name.islower():
        return False, "Skill name must be lowercase"

    # Check for valid characters (lowercase letters, numbers, hyphens)
    for char in name:
        if not (char.isalnum() or char == '-'):
            return False, "Skill name can only contain lowercase letters, numbers, and hyphens"

    if name.startswith('-') or name.endswith('-'):
        return False, "Skill name cannot start or end with a hyphen"

    return True, "Valid"


def create_structure(skill_name, location="personal"):
    """Create skill directory structure"""

    # Determine base path
    if location == "personal":
        base_path = Path.home() / ".claude" / "skills"
    elif location == "project":
        base_path = Path.cwd() / ".claude" / "skills"
    else:
        print(f"Error: Invalid location '{location}'. Use 'personal' or 'project'", file=sys.stderr)
        return False

    # Create skill directory
    skill_path = base_path / skill_name

    if skill_path.exists():
        print(f"Error: Skill directory already exists: {skill_path}", file=sys.stderr)
        return False

    try:
        # Create main directory
        skill_path.mkdir(parents=True, exist_ok=False)
        print(f"✓ Created skill directory: {skill_path}")

        # Create subdirectories
        subdirs = ["scripts", "references", "assets"]
        for subdir in subdirs:
            subdir_path = skill_path / subdir
            subdir_path.mkdir(exist_ok=True)
            print(f"✓ Created subdirectory: {subdir}/")

        # Create placeholder README in subdirectories
        (skill_path / "scripts" / "README.md").write_text(
            "# Scripts\n\nPlace executable scripts here for automation tasks.\n"
        )
        (skill_path / "references" / "README.md").write_text(
            "# References\n\nPlace supporting documentation here.\n"
        )
        (skill_path / "assets" / "README.md").write_text(
            "# Assets\n\nPlace templates, images, or binary files here.\n"
        )

        print(f"\n✓ Skill structure created successfully!")
        print(f"\nNext steps:")
        print(f"1. Generate SKILL.md: python3 scripts/generate-skill-template.py --name {skill_name}")
        print(f"2. Edit {skill_path}/SKILL.md to add instructions")
        print(f"3. Add scripts, references, and assets as needed")
        print(f"4. Validate: python3 scripts/validate-skill.py --path {skill_path}")

        return True

    except Exception as e:
        print(f"Error creating skill structure: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Create Claude Code skill directory structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Create personal skill
    python3 create-skill-structure.py --name commit-messages --location personal

    # Create project skill
    python3 create-skill-structure.py --name api-tester --location project
        """
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Skill name (lowercase, hyphens only, max 64 chars)"
    )

    parser.add_argument(
        "--location",
        choices=["personal", "project"],
        default="personal",
        help="Skill location: personal (~/.claude/skills) or project (.claude/skills)"
    )

    args = parser.parse_args()

    # Validate skill name
    is_valid, message = validate_skill_name(args.name)
    if not is_valid:
        print(f"Error: Invalid skill name - {message}", file=sys.stderr)
        sys.exit(1)

    # Create structure
    success = create_structure(args.name, args.location)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
