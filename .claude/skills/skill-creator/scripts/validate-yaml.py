#!/usr/bin/env python3
"""
Validate YAML frontmatter syntax

Usage:
    python3 validate-yaml.py --file SKILL.md
"""

import sys
import argparse
import yaml
from pathlib import Path


def validate_yaml_file(file_path):
    """Validate YAML frontmatter in SKILL.md"""

    try:
        content = Path(file_path).read_text()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return False

    # Check for frontmatter
    if not content.startswith('---'):
        print("Error: File must start with YAML frontmatter (---)", file=sys.stderr)
        return False

    # Extract frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        print("Error: YAML frontmatter not properly closed with ---", file=sys.stderr)
        return False

    frontmatter_text = parts[1]

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        print("✓ YAML syntax is valid")

        # Print parsed content
        print("\nParsed frontmatter:")
        print(yaml.dump(frontmatter, default_flow_style=False))

        return True

    except yaml.YAMLError as e:
        print(f"✗ YAML syntax error:", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter syntax in SKILL.md"
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to SKILL.md file"
    )

    args = parser.parse_args()

    success = validate_yaml_file(args.file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
