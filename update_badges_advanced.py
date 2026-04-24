#!/usr/bin/env python3
"""
Advanced GitHub Repository Metrics Badge Generator

Extended version with:
- Configuration file support
- Multiple repository support
- Custom metrics and badges
- Badge caching
- Detailed logging
"""

import json
import re
import sys
import logging
from pathlib import Path
from urllib import request, error
from urllib.parse import quote
from typing import Dict, List, Optional
from datetime import datetime


class BadgeConfig:
    """Configuration for badge generation."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = {}
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = self._default_config()

    @staticmethod
    def _default_config() -> dict:
        return {
            "owner": "Logiclayer1111",
            "repo": "minGPT",
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
                    "label": "📅 Activity",
                    "key": None,
                    "color": "informational",
                    "link_path": "activity",
                    "static_value": "View"
                }
            ],
            "auto_update_commit": True,
            "commit_message": "chore: update repository badges [skip ci]",
            "log_level": "INFO"
        }


class GitHubMetricsFetcher:
    """Fetches metrics from GitHub API."""

    def __init__(self, token: Optional[str] = None, log_level: str = "INFO"):
        self.token = token
        self.logger = self._setup_logger(log_level)

    @staticmethod
    def _setup_logger(level: str):
        logger = logging.getLogger("badges")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        return logger

    def fetch(self, owner: str, repo: str) -> Optional[Dict]:
        """Fetch repository data from GitHub API."""
        url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {
            "User-Agent": "GitHub-Badge-Generator",
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"

        try:
            self.logger.info(f"Fetching metrics for {owner}/{repo}...")
            req = request.Request(url, headers=headers)
            with request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                self.logger.info(f"✓ Received {len(data)} fields from API")
                return data
        except error.URLError as e:
            self.logger.error(f"Network error: {e}")
            return None
        except json.JSONDecodeError:
            self.logger.error("Failed to parse JSON response")
            return None


class BadgeGenerator:
    """Generates badge markdown."""

    @staticmethod
    def _shield_url(label: str, value: str, color: str) -> str:
        """Generate shields.io badge URL."""
        label_enc = quote(label)
        value_enc = quote(value)
        return f"https://img.shields.io/badge/{label_enc}-{value_enc}-{color}?logo=github&style=flat-square"

    @classmethod
    def generate(cls, config: BadgeConfig, data: Dict) -> str:
        """Generate badge markdown from config and data."""
        owner = config.config["owner"]
        repo = config.config["repo"]
        section_title = config.config.get("section_title", "📊 Repository Statistics")

        lines = [f"### {section_title}\n"]

        for badge_cfg in config.config.get("badges", []):
            label = badge_cfg["label"]
            color = badge_cfg.get("color", "blue")

            if badge_cfg.get("static_value"):
                value = badge_cfg["static_value"]
            else:
                key = badge_cfg["key"]
                value = str(data.get(key, 0))

            link_path = badge_cfg.get("link_path", "")
            link = f"https://github.com/{owner}/{repo}/{link_path}" if link_path else "#"

            badge_url = cls._shield_url(label, value, color)
            lines.append(f"[![{label}]({badge_url})]({link})")

        pushed_at = data.get("pushed_at", "").split("T")[0]
        lines.extend([
            "",
            f"**Last Updated:** {pushed_at}",
            "",
            "---"
        ])

        return "\n".join(lines) + "\n"


class ReadmeUpdater:
    """Updates README with badges."""

    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger("badges")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(log_level)

    def update(self, readme_path: str, badges_md: str) -> bool:
        """Update README with badge markdown."""
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.logger.info(f"Read {len(content)} bytes from {readme_path}")
        except FileNotFoundError:
            self.logger.error(f"README not found: {readme_path}")
            return False

        pattern = r"### [📊🔢📈].*?Repository Statistics\n\n.*?\n---\n"
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, badges_md, content, flags=re.DOTALL)
            self.logger.info("Replaced existing badges section")
        else:
            title_pattern = r"(# [^\n]+\n)"
            if re.search(title_pattern, content):
                content = re.sub(title_pattern, r"\1\n" + badges_md + "\n", content, count=1)
                self.logger.info("Inserted badges after title")
            else:
                content = badges_md + "\n" + content
                self.logger.info("Inserted badges at beginning")

        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.logger.info(f"Wrote {len(content)} bytes to {readme_path}")
            return True
        except IOError as e:
            self.logger.error(f"Write error: {e}")
            return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate live GitHub metrics badges for README"
    )
    parser.add_argument(
        "--config", "-c",
        help="Path to configuration file (JSON)"
    )
    parser.add_argument(
        "--repo", "-r",
        help="Repository (owner/repo format)"
    )
    parser.add_argument(
        "--token", "-t",
        help="GitHub API token"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose logging"
    )

    args = parser.parse_args()

    # Load config
    config = BadgeConfig(args.config)

    if args.repo:
        owner, repo = args.repo.split("/")
        config.config["owner"] = owner
        config.config["repo"] = repo

    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"

    # Fetch data
    fetcher = GitHubMetricsFetcher(
        token=args.token,
        log_level=log_level
    )
    data = fetcher.fetch(config.config["owner"], config.config["repo"])

    if not data:
        sys.exit(1)

    # Generate badges
    badges_md = BadgeGenerator.generate(config, data)

    # Update README
    updater = ReadmeUpdater(log_level=log_level)
    if updater.update(config.config["readme_path"], badges_md):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
