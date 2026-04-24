#!/usr/bin/env python3
"""
GitHub Repository Metrics Badge Generator

Fetches live data from GitHub API and generates dynamic badges for README.
Updates the README with shields.io badges linking to GitHub stats pages.

Usage:
    python update_badges.py

Environment:
    GITHUB_TOKEN (optional): GitHub API token for higher rate limits
"""

import json
import re
import sys
from pathlib import Path
from urllib import request, error
from urllib.parse import quote


def fetch_repo_data(owner: str, repo: str, token: str = None) -> dict:
    """Fetch repository data from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"

    headers = {
        "User-Agent": "GitHub-Badge-Generator",
        "Accept": "application/vnd.github.v3+json"
    }

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        req = request.Request(url, headers=headers)
        with request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except error.URLError as e:
        print(f"Error fetching GitHub API: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print("Error parsing GitHub API response", file=sys.stderr)
        return None


def generate_badge_markdown(owner: str, repo: str, data: dict) -> str:
    """Generate markdown section with badges."""

    stars = data.get("stargazers_count", 0)
    watchers = data.get("watchers_count", 0)
    forks = data.get("forks_count", 0)
    pushed_at = data.get("pushed_at", "").split("T")[0]

    # Create shield.io badge URLs with links
    badges = {
        "stars": {
            "label": "⭐ Stars",
            "value": str(stars),
            "link": f"https://github.com/{owner}/{repo}/stargazers"
        },
        "watchers": {
            "label": "👁️ Watchers",
            "value": str(watchers),
            "link": f"https://github.com/{owner}/{repo}/watchers"
        },
        "forks": {
            "label": "🍴 Forks",
            "value": str(forks),
            "link": f"https://github.com/{owner}/{repo}/network/members"
        },
        "activity": {
            "label": "📅 Activity",
            "value": "View",
            "link": f"https://github.com/{owner}/{repo}/activity"
        }
    }

    # Build markdown with badge links
    markdown = f"""### 📊 Repository Statistics

[![Stars]({_shield_url(badges['stars']['label'], badges['stars']['value'], 'blue')})]({badges['stars']['link']})
[![Watchers]({_shield_url(badges['watchers']['label'], badges['watchers']['value'], 'blue')})]({badges['watchers']['link']})
[![Forks]({_shield_url(badges['forks']['label'], badges['forks']['value'], 'blue')})]({badges['forks']['link']})
[![Activity]({_shield_url(badges['activity']['label'], badges['activity']['value'], 'informational')})]({badges['activity']['link']})

**Last Updated:** {pushed_at}

---
"""
    return markdown


def _shield_url(label: str, value: str, color: str) -> str:
    """Generate shields.io badge URL."""
    label_encoded = quote(label)
    value_encoded = quote(value)
    return f"https://img.shields.io/badge/{label_encoded}-{value_encoded}-{color}?logo=github&style=flat-square"


def update_readme(readme_path: str, badges_markdown: str, owner: str, repo: str) -> bool:
    """Update README.md with new badges section."""

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"README.md not found at {readme_path}", file=sys.stderr)
        return False

    # Pattern to find and replace the stats section (simplified to avoid emoji issues)
    pattern = r"### 📊 Repository Statistics\n\n.*?\n---\n"

    if re.search(pattern, content, re.DOTALL):
        # Replace existing section
        content = re.sub(pattern, badges_markdown, content, flags=re.DOTALL)
    else:
        # Insert after title if no existing section
        title_pattern = r"(# [^\n]+\n)"
        if re.search(title_pattern, content):
            content = re.sub(title_pattern, r"\1\n" + badges_markdown + "\n", content, count=1)
        else:
            # Fallback: insert at beginning
            content = badges_markdown + "\n" + content

    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"Error writing to README.md: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point."""

    # Configuration
    owner = "Logiclayer1111"
    repo = "minGPT"
    readme_path = Path(__file__).parent / "README.md"

    print(f"Fetching repository data for {owner}/{repo}...")
    data = fetch_repo_data(owner, repo)

    if not data:
        print("Failed to fetch repository data", file=sys.stderr)
        return 1

    print(f"[+] Stars: {data.get('stargazers_count', 0)}")
    print(f"[+] Watchers: {data.get('watchers_count', 0)}")
    print(f"[+] Forks: {data.get('forks_count', 0)}")

    badges_md = generate_badge_markdown(owner, repo, data)

    if update_readme(str(readme_path), badges_md, owner, repo):
        print(f"[+] Updated README.md with live badges")
        return 0
    else:
        print("Failed to update README.md", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
