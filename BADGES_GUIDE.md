# GitHub Metrics Badge Auto-Update Guide

This guide shows you how to automatically update GitHub repository metrics badges in your README.

## Quick Start

### Manual Update (Python)

```bash
python update_badges.py
```

### Manual Update (Node.js)

```bash
node update_badges.js
```

## What Gets Updated

The scripts fetch from GitHub API and generate live badges with links:

- **⭐ Stars** → Links to `/stargazers` page
- **👁️ Watchers** → Links to `/watchers` page  
- **🍴 Forks** → Links to `/network/members` page
- **📅 Activity** → Links to `/activity` page

## Automated Updates with GitHub Actions

### Option 1: Daily Updates

Create `.github/workflows/update-badges.yml`:

```yaml
name: Update README Badges

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight UTC
  workflow_dispatch:      # Allow manual trigger

jobs:
  update-badges:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Update badges
        run: python update_badges.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Commit and push if changed
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          if git diff --quiet README.md; then
            echo "No changes to commit"
          else
            git add README.md
            git commit -m "chore: update repository badges"
            git push
          fi
```

### Option 2: On Each Push to Master

```yaml
name: Update README Badges

on:
  push:
    branches: [ master ]
    paths:
      - '.github/workflows/update-badges.yml'
  workflow_dispatch:

jobs:
  update-badges:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: python update_badges.py
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'chore: update repository badges'
          file_pattern: README.md
```

## Using GitHub Token

For higher rate limits (5,000 requests/hour instead of 60), set a personal access token:

1. Go to GitHub Settings → Personal access tokens → Tokens (classic)
2. Create token with `public_repo` scope
3. Add to repository secrets as `GH_TOKEN`
4. Use in workflow: `GITHUB_TOKEN: ${{ secrets.GH_TOKEN }}`

Or set locally:

```bash
export GITHUB_TOKEN=your_token_here
python update_badges.py
```

## Examples

### Markdown Output

```markdown
### 📊 Repository Statistics

[![Stars](https://img.shields.io/badge/⭐%20Stars-42-blue?logo=github&style=flat-square)](https://github.com/Logiclayer1111/minGPT/stargazers)
[![Watchers](https://img.shields.io/badge/👁️%20Watchers-8-blue?logo=github&style=flat-square)](https://github.com/Logiclayer1111/minGPT/watchers)
[![Forks](https://img.shields.io/badge/🍴%20Forks-5-blue?logo=github&style=flat-square)](https://github.com/Logiclayer1111/minGPT/network/members)
[![Activity](https://img.shields.io/badge/📅%20Activity-View-informational?logo=github&style=flat-square)](https://github.com/Logiclayer1111/minGPT/activity)

**Last Updated:** 2026-04-24

---
```

## Customization

### Change Badge Colors

Edit the color values in `update_badges.py` or `update_badges.js`:

```python
"stars": {
    # ... 
    "link": ...,
    "color": "green"  # Change from "blue"
}
```

Shields.io supports: `blue`, `green`, `red`, `yellow`, `informational`, `success`, `critical`, etc.

### Add More Metrics

Extend `generate_badge_markdown()` to include additional metrics:

```python
"issues": {
    "label": "📋 Issues",
    "value": str(data.get("open_issues_count", 0)),
    "link": f"https://github.com/{owner}/{repo}/issues"
}
```

### Custom Repository

Change owner/repo in the main section:

```python
owner = "your-username"
repo = "your-repo-name"
```

## Troubleshooting

### "No such file or directory: README.md"

Ensure you're running from the repository root:

```bash
cd your-repo
python update_badges.py
```

### "Failed to fetch repository data"

Check your GitHub token is valid and has access to the repository:

```bash
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/owner/repo
```

### Rate Limiting

GitHub API has limits:
- **Without token**: 60 requests/hour
- **With token**: 5,000 requests/hour

Add your token to `.env` or use environment variables.

### Encoding Errors on Windows

The scripts handle UTF-8 encoding. If issues persist:

```bash
python -c "import sys; print(sys.stdout.encoding)"
```

Should output `utf-8`. If not, set:

```cmd
set PYTHONIOENCODING=utf-8
```

## CI/CD Integration

These badges update automatically on:
- Daily schedule (midnight UTC)
- Manual workflow trigger
- Push to master (optional)

Commits are made with bot account, so they don't trigger additional workflows.

## Reference

- [GitHub REST API - Repositories](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28)
- [Shields.io Badge Service](https://shields.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
