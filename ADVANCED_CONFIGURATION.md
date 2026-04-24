# Advanced Badge Configuration Guide

## Overview

The advanced badge system provides:
- ✅ Configuration file support (JSON)
- ✅ Multiple badges per repository
- ✅ Custom colors and metrics
- ✅ Flexible badge ordering
- ✅ Detailed logging
- ✅ Command-line arguments
- ✅ Static value badges

## Usage

### Basic Usage with Config File

```bash
python update_badges_advanced.py --config badges.config.json
```

### Command-Line Overrides

Override specific settings without modifying config file:

```bash
# Change repository
python update_badges_advanced.py --repo user/another-repo

# Use personal access token
python update_badges_advanced.py --token ghp_xxxxxxxxxxxx

# Verbose logging
python update_badges_advanced.py --verbose
```

### All Options

```bash
python update_badges_advanced.py --help
```

Output:
```
-c, --config    Path to configuration file (JSON)
-r, --repo      Repository (owner/repo format)
-t, --token     GitHub API token
-v, --verbose   Verbose logging (DEBUG level)
```

## Configuration File

### Structure

```json
{
  "owner": "username",
  "repo": "repository",
  "readme_path": "README.md",
  "section_title": "📊 Repository Statistics",
  "badges": [
    {
      "label": "Badge Label",
      "key": "api_field_name",
      "color": "blue",
      "link_path": "github/page/path"
    }
  ],
  "log_level": "INFO"
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `owner` | string | GitHub username or organization |
| `repo` | string | Repository name |
| `readme_path` | string | Path to README.md |
| `section_title` | string | Section heading (supports emojis) |
| `badges` | array | Badge definitions |
| `log_level` | string | `INFO`, `DEBUG`, `WARNING`, `ERROR` |

### Badge Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `label` | string | ✅ | Badge label text (emoji + text) |
| `key` | string | ⚠️ | GitHub API field name (null for static values) |
| `color` | string | ✅ | shields.io color (`blue`, `green`, `red`, `yellow`, `orange`, `informational`, `success`, `critical`) |
| `link_path` | string | ✅ | GitHub page path (e.g., `stargazers`, `issues`, `activity`) |
| `static_value` | string | ❌ | Static text instead of API value (for non-metric badges) |

## Examples

### Example 1: Custom Color Badges

```json
{
  "owner": "myuser",
  "repo": "myrepo",
  "badges": [
    {
      "label": "⭐ Stars",
      "key": "stargazers_count",
      "color": "green",
      "link_path": "stargazers"
    },
    {
      "label": "🍴 Forks",
      "key": "forks_count",
      "color": "critical",
      "link_path": "network/members"
    }
  ]
}
```

### Example 2: Extended Metrics

```json
{
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
      "key": null,
      "static_value": "View",
      "color": "informational",
      "link_path": "contributors"
    },
    {
      "label": "📅 Activity",
      "key": null,
      "static_value": "View",
      "color": "informational",
      "link_path": "activity"
    }
  ]
}
```

### Example 3: Minimal Config

```json
{
  "owner": "myuser",
  "repo": "myrepo",
  "badges": [
    {
      "label": "⭐ Stars",
      "key": "stargazers_count",
      "color": "blue",
      "link_path": "stargazers"
    }
  ]
}
```

## Available API Fields

Common fields from GitHub API:

```
stargazers_count       - Number of stars
watchers_count         - Number of watchers
forks_count            - Number of forks
open_issues_count      - Number of open issues
network_count          - Number in network
subscribers_count      - Number of subscribers
size                   - Repository size
language               - Primary language
created_at             - Creation date
updated_at             - Last update date
pushed_at              - Last push date
```

## Available Colors

shields.io badge colors:

```
blue              - Default
green             - Success/good
red               - Failure/error
yellow            - Warning/attention
orange            - Important
brightgreen       - Very good
informational     - Information
success           - Success (alt)
critical          - Critical error
lightgrey         - Neutral
555               - Dark grey
```

## Logging Levels

```
DEBUG    - Detailed diagnostic information
INFO     - General informational messages (default)
WARNING  - Warning messages
ERROR    - Error messages
```

Enable with:
```bash
python update_badges_advanced.py --verbose  # DEBUG level
```

## GitHub API Fields Reference

Complete list of available fields:

```json
{
  "stargazers_count": 100,
  "watchers_count": 100,
  "forks_count": 50,
  "open_issues_count": 5,
  "open_issues": 5,
  "watchers": 100,
  "network_count": 50,
  "subscribers_count": 10,
  "size": 1024,
  "language": "Python",
  "created_at": "2020-01-01T00:00:00Z",
  "updated_at": "2024-04-24T00:00:00Z",
  "pushed_at": "2024-04-24T00:00:00Z"
}
```

## Integration Examples

### GitHub Actions with Config

```yaml
- name: Update badges with config
  run: |
    python update_badges_advanced.py --config badges.config.json
```

### Multiple Repositories

Create separate config files:

```bash
mkdir badge-configs
cat > badge-configs/repo1.json << EOF
{
  "owner": "user",
  "repo": "repo1",
  ...
}
EOF

python update_badges_advanced.py --config badge-configs/repo1.json
```

### Custom Section Title

Edit `badges.config.json`:

```json
{
  "section_title": "📈 GitHub Stats"
}
```

## Tips & Tricks

### Ordering Badges

Order badges by editing the `badges` array in config:

```json
{
  "badges": [
    { stars },
    { watchers },
    { forks },
    { issues }
  ]
}
```

### Static Badges (No API Call)

Use `"key": null` and `"static_value"`:

```json
{
  "label": "📝 Docs",
  "key": null,
  "static_value": "Read",
  "color": "blue",
  "link_path": "wiki"
}
```

### Conditional Colors

Modify script to check values and set colors dynamically:

```python
color = "red" if data.get("open_issues_count", 0) > 20 else "yellow"
```

## Troubleshooting

### Config Not Found

```
Error: No such file or directory
```

Solution: Use absolute path or run from same directory as config file.

### Invalid JSON

```
Error: Failed to parse JSON response
```

Validate JSON:
```bash
python -m json.tool badges.config.json
```

### Rate Limiting

Add GitHub token to increase limit:
```bash
python update_badges_advanced.py --token YOUR_TOKEN
```

### No Changes

If README isn't updating:
1. Check `readme_path` in config
2. Verify section title matches regex
3. Run with `--verbose` to see details

## Migration from Simple Version

Simple version:
```bash
python update_badges.py
```

Advanced version with defaults:
```bash
python update_badges_advanced.py
```

Advanced version with custom config:
```bash
python update_badges_advanced.py --config my-config.json
```

All versions are compatible and can be used interchangeably.
