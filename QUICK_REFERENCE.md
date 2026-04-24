# GitHub Metrics Badges - Quick Reference

## What's Included

```
update_badges.py                 - Simple Python script (recommended for most users)
update_badges.js                 - Node.js version
update_badges_advanced.py        - Advanced version with config file support
badge_utils.py                   - Utility tools (validate, preview, generate configs)
badges.config.json               - Configuration file example
.github/workflows/update-badges.yml - GitHub Actions automation
BADGES_GUIDE.md                  - Full setup documentation
ADVANCED_CONFIGURATION.md        - Advanced options and examples
```

## Getting Started (30 seconds)

### Run Once
```bash
# Update README with live badges
python update_badges.py
```

### Set Up Automation
```bash
# Push these files to GitHub and badges update daily
git add .github/workflows/update-badges.yml update_badges.py
git commit -m "Add badge automation"
git push
```

## Badge Comparison

| Feature | Simple | Advanced |
|---------|--------|----------|
| Speed | ⚡ Fast | ⚡ Fast |
| Setup | 0 config | 1 JSON file |
| Customization | Limited | Extensive |
| Multiple repos | No | Yes |
| CLI options | No | Yes |
| Logging | Basic | Detailed |

### Use Simple Version If:
- ✅ First time using badges
- ✅ Single repository
- ✅ Happy with default colors
- ✅ Want minimal dependencies

### Use Advanced Version If:
- ✅ Need custom colors
- ✅ Managing multiple repos
- ✅ Want detailed logging
- ✅ Prefer config files

## Commands Reference

### Simple Version
```bash
# Manual update
python update_badges.py

# With GitHub token (higher rate limit)
GITHUB_TOKEN=ghp_xxxx python update_badges.py
```

### Advanced Version
```bash
# With default config
python update_badges_advanced.py

# With custom config
python update_badges_advanced.py --config my-config.json

# Override repository
python update_badges_advanced.py --repo user/repo

# With token
python update_badges_advanced.py --token ghp_xxxx

# Verbose output
python update_badges_advanced.py --verbose
```

### Node.js Version
```bash
# Manual update
node update_badges.js

# With token
GITHUB_TOKEN=ghp_xxxx node update_badges.js
```

### Utility Tools
```bash
# Validate config
python badge_utils.py validate badges.config.json

# Generate config from template
python badge_utils.py generate standard -o my-config.json
python badge_utils.py generate extended -o my-config.json
python badge_utils.py generate minimal -o my-config.json

# Preview badges
python badge_utils.py preview badges.config.json
```

## Configuration

### Quick Config (Standard Badges)
```json
{
  "owner": "your-username",
  "repo": "your-repository",
  "readme_path": "README.md"
}
```

### Full Config (All Options)
```json
{
  "owner": "your-username",
  "repo": "your-repository",
  "readme_path": "README.md",
  "section_title": "📊 Repository Statistics",
  "badges": [
    {
      "label": "⭐ Stars",
      "key": "stargazers_count",
      "color": "blue",
      "link_path": "stargazers"
    }
  ],
  "log_level": "INFO"
}
```

## Badges Generated

```
⭐ Stars     → links to /stargazers
👁️ Watchers   → links to /watchers
🍴 Forks     → links to /network/members
📋 Issues    → links to /issues
📅 Activity  → links to /activity
```

## Colors Available

```
blue, green, red, yellow, orange, brightgreen,
informational, success, critical, lightgrey
```

## GitHub Actions Setup

Already included in `.github/workflows/update-badges.yml`

### Manual Setup
1. Copy `.github/workflows/update-badges.yml` to your repo
2. Commit and push
3. Badges auto-update daily

### Manual Trigger
Go to **Actions** → **Update Repository Badges** → **Run workflow**

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "File not found" | Run from repo root, check `readme_path` |
| "API error" | Add `GITHUB_TOKEN` for higher rate limit |
| "No changes" | Check section title matches, run with `--verbose` |
| "Encoding error" | Usually fixed automatically, try `python -u` |

## Performance

- API calls: ~100ms
- File I/O: ~10ms
- Total: <500ms
- Safe to run 100+ times/day

## Rate Limits

```
Without token: 60 requests/hour
With token:    5,000 requests/hour
```

For daily updates (1 request/day), token not needed.

## Examples

### Example 1: Simple Update
```bash
python update_badges.py
# Done! README.md updated
```

### Example 2: Custom Colors
Edit `badges.config.json`:
```json
{
  "badges": [
    {
      "label": "⭐ Stars",
      "color": "green"
    }
  ]
}
```
Then:
```bash
python update_badges_advanced.py --config badges.config.json
```

### Example 3: Automation
```bash
# Push workflow file
git add .github/workflows/update-badges.yml
git commit -m "Add badge automation"
git push
# Done! Badges update daily at midnight UTC
```

### Example 4: Preview Before Updating
```bash
python badge_utils.py preview badges.config.json
# Shows what badges will look like
```

### Example 5: New Config
```bash
python badge_utils.py generate extended -o my-badges.json
# Edit my-badges.json
python badge_utils_advanced.py --config my-badges.json
```

## File Purposes

| File | Purpose |
|------|---------|
| `update_badges.py` | Primary script - simple and fast |
| `update_badges.js` | Node.js alternative (no deps) |
| `update_badges_advanced.py` | Config-file driven, multiple repos |
| `badge_utils.py` | Validate, preview, generate configs |
| `badges.config.json` | Example configuration |
| `BADGES_GUIDE.md` | Full documentation |
| `ADVANCED_CONFIGURATION.md` | Advanced options |
| `.github/workflows/update-badges.yml` | GitHub Actions automation |

## Environment Variables

```bash
GITHUB_TOKEN          # GitHub API token (optional)
PYTHONIOENCODING=utf-8 # Fix encoding on Windows (optional)
```

## Integration with CI/CD

### GitHub Actions
Already setup in `.github/workflows/update-badges.yml`

### Manual CI/CD
```bash
# In your CI pipeline
python update_badges.py
git add README.md
git commit -m "chore: update badges"
git push
```

### Docker
```bash
docker run -v $(pwd):/repo python:3.11 \
  bash -c "cd /repo && python update_badges.py"
```

## Common Tasks

### Update badges right now
```bash
python update_badges.py
```

### Schedule daily updates
```bash
# Already done! GitHub Actions runs daily.
# Or manually with cron:
0 0 * * * cd /path/to/repo && python update_badges.py
```

### Change badge colors
```bash
# Edit badges.config.json
python badge_utils.py generate standard -o badges.config.json
# Edit the "color" fields
python update_badges_advanced.py --config badges.config.json
```

### Add more metrics
```bash
# Edit badges.config.json and add to "badges" array
# Examples: open_issues_count, subscribers_count, forks_count, language
```

### Use different repository
```bash
python update_badges_advanced.py --repo other-user/other-repo
```

## Next Steps

1. **Immediate**: Run `python update_badges.py`
2. **Today**: Commit and push all files
3. **Maintenance**: Badges update automatically daily
4. **Optional**: Read `ADVANCED_CONFIGURATION.md` for customization

## Support

- 📖 Read `BADGES_GUIDE.md` for detailed setup
- 🔧 Read `ADVANCED_CONFIGURATION.md` for advanced options
- ✅ Use `badge_utils.py validate` to check configs
- 👀 Use `badge_utils.py preview` to see badges before updating

## License

These scripts are standalone utilities - use as-is or customize freely.
