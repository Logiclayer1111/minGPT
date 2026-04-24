#!/usr/bin/env python3
"""
Badge Utilities - Helper tools for badge management

Features:
- Validate configuration files
- Generate sample configurations
- Preview badges without updating README
- Batch update multiple repositories
"""

import json
import sys
import argparse
from pathlib import Path
from urllib.parse import quote


class BadgeValidator:
    """Validates badge configuration files."""

    REQUIRED_FIELDS = {"owner", "repo", "readme_path"}
    BADGE_REQUIRED = {"label", "color", "link_path"}
    VALID_COLORS = {
        "blue", "green", "red", "yellow", "orange", "brightgreen",
        "informational", "success", "critical", "lightgrey", "555"
    }

    @classmethod
    def validate_config(cls, config_path: str) -> tuple[bool, list[str]]:
        """Validate configuration file."""
        errors = []

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            return False, [f"Config file not found: {config_path}"]
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]

        # Check required fields
        for field in cls.REQUIRED_FIELDS:
            if field not in config:
                errors.append(f"Missing required field: {field}")

        # Check badges
        if "badges" not in config:
            errors.append("Missing required field: badges")
        elif not isinstance(config["badges"], list):
            errors.append("Badges must be a list")
        else:
            for i, badge in enumerate(config["badges"]):
                badge_errors = cls._validate_badge(badge, i)
                errors.extend(badge_errors)

        return len(errors) == 0, errors

    @staticmethod
    def _validate_badge(badge: dict, index: int) -> list[str]:
        """Validate a single badge configuration."""
        errors = []

        required = {"label", "color", "link_path"}
        for field in required:
            if field not in badge:
                errors.append(f"Badge[{index}] missing {field}")

        if "color" in badge and badge["color"] not in BadgeValidator.VALID_COLORS:
            errors.append(f"Badge[{index}] invalid color: {badge['color']}")

        if "key" not in badge and "static_value" not in badge:
            errors.append(f"Badge[{index}] must have 'key' or 'static_value'")

        return errors


class SampleConfigGenerator:
    """Generates sample configuration files."""

    @staticmethod
    def minimal() -> dict:
        """Minimal configuration."""
        return {
            "owner": "username",
            "repo": "repository",
            "readme_path": "README.md",
            "badges": [
                {
                    "label": "⭐ Stars",
                    "key": "stargazers_count",
                    "color": "blue",
                    "link_path": "stargazers"
                }
            ]
        }

    @staticmethod
    def standard() -> dict:
        """Standard configuration with common badges."""
        return {
            "owner": "username",
            "repo": "repository",
            "readme_path": "README.md",
            "section_title": "📊 Repository Statistics",
            "badges": [
                {
                    "label": "⭐ Stars",
                    "key": "stargazers_count",
                    "color": "blue",
                    "link_path": "stargazers"
                },
                {
                    "label": "👁️ Watchers",
                    "key": "watchers_count",
                    "color": "blue",
                    "link_path": "watchers"
                },
                {
                    "label": "🍴 Forks",
                    "key": "forks_count",
                    "color": "blue",
                    "link_path": "network/members"
                },
                {
                    "label": "📋 Issues",
                    "key": "open_issues_count",
                    "color": "yellow",
                    "link_path": "issues"
                }
            ],
            "log_level": "INFO"
        }

    @staticmethod
    def extended() -> dict:
        """Extended configuration with all available badges."""
        return {
            "owner": "username",
            "repo": "repository",
            "readme_path": "README.md",
            "section_title": "📊 Repository Statistics",
            "badges": [
                {
                    "label": "⭐ Stars",
                    "key": "stargazers_count",
                    "color": "blue",
                    "link_path": "stargazers"
                },
                {
                    "label": "👁️ Watchers",
                    "key": "watchers_count",
                    "color": "blue",
                    "link_path": "watchers"
                },
                {
                    "label": "🍴 Forks",
                    "key": "forks_count",
                    "color": "blue",
                    "link_path": "network/members"
                },
                {
                    "label": "📋 Issues",
                    "key": "open_issues_count",
                    "color": "yellow",
                    "link_path": "issues"
                },
                {
                    "label": "👥 Contributors",
                    "key": None,
                    "static_value": "View",
                    "color": "informational",
                    "link_path": "contributors"
                },
                {
                    "label": "📅 Activity",
                    "key": None,
                    "static_value": "View",
                    "color": "informational",
                    "link_path": "activity"
                }
            ],
            "log_level": "INFO"
        }


class BadgePreview:
    """Generates badge previews."""

    @staticmethod
    def shield_url(label: str, value: str, color: str) -> str:
        """Generate shields.io URL."""
        label_enc = quote(label)
        value_enc = quote(value)
        return f"https://img.shields.io/badge/{label_enc}-{value_enc}-{color}?logo=github&style=flat-square"

    @classmethod
    def preview_badge(cls, label: str, value: str, color: str, link: str) -> str:
        """Generate markdown for a single badge."""
        url = cls.shield_url(label, value, color)
        return f"[![{label}]({url})]({link})"

    @classmethod
    def preview_badges(cls, config: dict, sample_data: dict) -> str:
        """Generate preview of all badges."""
        owner = config["owner"]
        repo = config["repo"]
        lines = []

        for badge_cfg in config.get("badges", []):
            label = badge_cfg["label"]
            color = badge_cfg.get("color", "blue")

            if badge_cfg.get("static_value"):
                value = badge_cfg["static_value"]
            else:
                key = badge_cfg.get("key", "")
                value = str(sample_data.get(key, "0"))

            link_path = badge_cfg.get("link_path", "")
            link = f"https://github.com/{owner}/{repo}/{link_path}" if link_path else "#"

            lines.append(cls.preview_badge(label, value, color, link))

        return "\n".join(lines)


def main():
    """Main entry point."""
    # Fix encoding on Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description="Badge utility tools"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate config file")
    validate_parser.add_argument("config", help="Config file path")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate sample config")
    gen_parser.add_argument(
        "template",
        choices=["minimal", "standard", "extended"],
        help="Template type"
    )
    gen_parser.add_argument(
        "-o", "--output",
        help="Output file (default: stdout)"
    )

    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Preview badges")
    preview_parser.add_argument("config", help="Config file path")

    args = parser.parse_args()

    if args.command == "validate":
        valid, errors = BadgeValidator.validate_config(args.config)
        if valid:
            print("[+] Config is valid")
            return 0
        else:
            print("[-] Config is invalid:")
            for error in errors:
                print(f"  - {error}")
            return 1

    elif args.command == "generate":
        generator_method = getattr(SampleConfigGenerator, args.template)
        config = generator_method()

        output = json.dumps(config, indent=2, ensure_ascii=False)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"[+] Wrote sample config to {args.output}")
        else:
            print(output)
        return 0

    elif args.command == "preview":
        try:
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"[-] Error reading config: {e}")
            return 1

        sample_data = {
            "stargazers_count": 42,
            "watchers_count": 8,
            "forks_count": 5,
            "open_issues_count": 2
        }

        print("[+] Badge Preview:\n")
        print(BadgePreview.preview_badges(config, sample_data))
        return 0

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
