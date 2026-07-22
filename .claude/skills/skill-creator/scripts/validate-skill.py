#!/usr/bin/env python3
"""
Validate Claude Code skill structure and content

Usage:
    python3 validate-skill.py --path PATH_TO_SKILL [--verbose]
"""

import sys
import os
import argparse
import re
from pathlib import Path
import yaml


class SkillValidator:
    def __init__(self, skill_path, verbose=False):
        self.skill_path = Path(skill_path)
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.info = []

    def log_error(self, message):
        self.errors.append(message)
        if self.verbose:
            print(f"✗ ERROR: {message}", file=sys.stderr)

    def log_warning(self, message):
        self.warnings.append(message)
        if self.verbose:
            print(f"⚠ WARNING: {message}")

    def log_info(self, message):
        self.info.append(message)
        if self.verbose:
            print(f"ℹ INFO: {message}")

    def validate_structure(self):
        """Validate directory structure"""
        self.log_info("Validating directory structure...")

        # Check if path exists
        if not self.skill_path.exists():
            self.log_error(f"Skill path does not exist: {self.skill_path}")
            return False

        # Check for SKILL.md
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.log_error("SKILL.md not found")
            return False
        else:
            self.log_info("✓ SKILL.md found")

        # Check optional directories
        for subdir in ["scripts", "references", "assets"]:
            subdir_path = self.skill_path / subdir
            if subdir_path.exists():
                self.log_info(f"✓ {subdir}/ directory found")
            else:
                self.log_info(f"  {subdir}/ directory not present (optional)")

        return True

    def validate_frontmatter(self, content):
        """Validate YAML frontmatter"""
        self.log_info("Validating YAML frontmatter...")

        # Extract frontmatter
        if not content.startswith('---'):
            self.log_error("SKILL.md must start with YAML frontmatter (---)")
            return False

        # Find closing ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            self.log_error("YAML frontmatter not properly closed with ---")
            return False

        frontmatter_text = parts[1]

        # Parse YAML
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            self.log_error(f"Invalid YAML syntax: {e}")
            return False

        # Validate required fields
        if 'name' not in frontmatter:
            self.log_error("Missing required field: name")
            return False

        if 'description' not in frontmatter:
            self.log_error("Missing required field: description")
            return False

        # Validate name field
        name = frontmatter['name']
        if not isinstance(name, str):
            self.log_error("name field must be a string")
            return False

        if len(name) > 64:
            self.log_error(f"name field exceeds 64 characters (found: {len(name)})")
            return False

        if not name.islower():
            self.log_error("name field must be lowercase")
            return False

        if not re.match(r'^[a-z0-9-]+$', name):
            self.log_error("name field can only contain lowercase letters, numbers, and hyphens")
            return False

        if name.startswith('-') or name.endswith('-'):
            self.log_error("name field cannot start or end with a hyphen")
            return False

        self.log_info(f"✓ Valid name: {name}")

        # Validate description field
        description = frontmatter['description']
        if not isinstance(description, str):
            self.log_error("description field must be a string")
            return False

        if len(description) > 1024:
            self.log_error(f"description exceeds 1024 characters (found: {len(description)})")
            return False

        if not description.strip():
            self.log_error("description cannot be empty")
            return False

        if '<' in description or '>' in description:
            self.log_error("description cannot contain XML tags")
            return False

        self.log_info(f"✓ Valid description ({len(description)} chars)")

        # Check for trigger keywords
        action_verbs = ['create', 'generate', 'analyze', 'test', 'validate', 'process', 'extract', 'convert', 'review']
        has_action_verb = any(verb in description.lower() for verb in action_verbs)
        if not has_action_verb:
            self.log_warning("description should include action verbs (create, generate, analyze, etc.)")

        # Validate optional fields
        if 'version' in frontmatter:
            version = frontmatter['version']
            if not re.match(r'^\d+\.\d+\.\d+', str(version)):
                self.log_warning("version should follow semantic versioning (e.g., 1.0.0)")

        if 'allowed-tools' in frontmatter:
            tools = frontmatter['allowed-tools']
            if isinstance(tools, str):
                self.log_info(f"✓ allowed-tools: {tools}")
            else:
                self.log_warning("allowed-tools should be a comma-separated string")

        return True

    def validate_content(self, content):
        """Validate content structure"""
        self.log_info("Validating content structure...")

        # Extract content (after frontmatter)
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False

        main_content = parts[2]

        # Check for required sections
        required_sections = [
            ("Overview", r'##\s+Overview'),
            ("When to Use", r'##\s+When to Use'),
            ("Instructions", r'##\s+Instructions'),
            ("Examples", r'##\s+Examples'),
        ]

        for section_name, pattern in required_sections:
            if re.search(pattern, main_content, re.IGNORECASE):
                self.log_info(f"✓ {section_name} section found")
            else:
                self.log_warning(f"{section_name} section not found (recommended)")

        # Check content length
        line_count = len(main_content.split('\n'))
        self.log_info(f"Content length: {line_count} lines")

        if line_count > 500:
            self.log_warning(f"Content is long ({line_count} lines). Consider under 500 lines for optimal performance.")

        # Check for code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', main_content)
        if code_blocks:
            self.log_info(f"✓ Found {len(code_blocks)} code block(s)")

        # Check for file references
        file_refs = re.findall(r'`(?:scripts|references|assets)/[^`]+`', main_content)
        if file_refs:
            self.log_info(f"✓ Found {len(file_refs)} file reference(s)")
            for ref in file_refs:
                # Extract path (remove backticks)
                ref_path = ref.strip('`')
                full_path = self.skill_path / ref_path
                if not full_path.exists():
                    self.log_warning(f"Referenced file not found: {ref_path}")

        return True

    def validate_scripts(self):
        """Validate scripts directory"""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return True

        self.log_info("Validating scripts...")

        scripts = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))

        if not scripts:
            self.log_info("  No scripts found in scripts/ directory")
            return True

        for script in scripts:
            # Check if executable
            if not os.access(script, os.X_OK):
                self.log_warning(f"Script not executable: {script.name} (run: chmod +x {script})")

            # Check for shebang
            try:
                first_line = script.read_text().split('\n')[0]
                if not first_line.startswith('#!'):
                    self.log_warning(f"Script missing shebang line: {script.name}")
                else:
                    self.log_info(f"✓ {script.name} has shebang")
            except Exception as e:
                self.log_warning(f"Could not read script: {script.name} - {e}")

        return True

    def validate(self):
        """Run all validations"""
        print(f"Validating skill at: {self.skill_path}\n")

        # Structure validation
        if not self.validate_structure():
            return False

        # Read SKILL.md
        skill_md_path = self.skill_path / "SKILL.md"
        try:
            content = skill_md_path.read_text()
        except Exception as e:
            self.log_error(f"Could not read SKILL.md: {e}")
            return False

        # Frontmatter validation
        if not self.validate_frontmatter(content):
            return False

        # Content validation
        if not self.validate_content(content):
            return False

        # Scripts validation
        if not self.validate_scripts():
            return False

        return True

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        if self.errors:
            print(f"\n✗ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠ WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✓ ALL VALIDATIONS PASSED")
            print("\nYour skill is ready to use!")
            print("\nNext steps:")
            print("1. Test the skill by restarting Claude Code")
            print("2. Try activating with trigger keywords from description")
            print("3. Verify instructions are followable")
            print("4. Iterate based on real usage")
        elif not self.errors:
            print("\n✓ VALIDATION PASSED (with warnings)")
            print("\nYour skill is functional but consider addressing warnings for best results.")
        else:
            print("\n✗ VALIDATION FAILED")
            print("\nPlease fix the errors above before using this skill.")

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Claude Code skill structure and content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Validate personal skill
    python3 validate-skill.py --path ~/.claude/skills/commit-messages

    # Validate project skill with verbose output
    python3 validate-skill.py --path .claude/skills/api-tester --verbose
        """
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Path to skill directory containing SKILL.md"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed validation progress"
    )

    args = parser.parse_args()

    # Create validator
    validator = SkillValidator(args.path, args.verbose)

    # Run validation
    success = validator.validate()

    # Print summary
    validator.print_summary()

    # Exit with appropriate code
    sys.exit(0 if success and not validator.errors else 1)


if __name__ == "__main__":
    main()
