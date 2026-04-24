#!/usr/bin/env node

/**
 * GitHub Repository Metrics Badge Generator (JavaScript version)
 *
 * Fetches live data from GitHub API and generates dynamic badges for README.
 *
 * Usage:
 *   npx node update_badges.js
 *
 * Environment:
 *   GITHUB_TOKEN (optional): GitHub API token for higher rate limits
 */

const fs = require("fs");
const path = require("path");
const https = require("https");

function fetchRepoData(owner, repo, token = null) {
  return new Promise((resolve, reject) => {
    const url = `https://api.github.com/repos/${owner}/${repo}`;

    const headers = {
      "User-Agent": "GitHub-Badge-Generator",
      Accept: "application/vnd.github.v3+json",
    };

    if (token) {
      headers.Authorization = `token ${token}`;
    }

    https
      .get(url, { headers }, (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode === 200) {
            try {
              resolve(JSON.parse(data));
            } catch (e) {
              reject(new Error("Failed to parse GitHub API response"));
            }
          } else {
            reject(
              new Error(`GitHub API error: ${res.statusCode} ${res.statusMessage}`)
            );
          }
        });
      })
      .on("error", (e) => reject(e));
  });
}

function encodeUrl(str) {
  return encodeURIComponent(str).replace(/!/g, "%21").replace(/'/g, "%27");
}

function shieldUrl(label, value, color) {
  const labelEncoded = encodeUrl(label);
  const valueEncoded = encodeUrl(value);
  return `https://img.shields.io/badge/${labelEncoded}-${valueEncoded}-${color}?logo=github&style=flat-square`;
}

function generateBadgeMarkdown(owner, repo, data) {
  const stars = data.stargazers_count || 0;
  const watchers = data.watchers_count || 0;
  const forks = data.forks_count || 0;
  const pushedAt = (data.pushed_at || "").split("T")[0];

  const badges = {
    stars: {
      label: "⭐ Stars",
      value: String(stars),
      link: `https://github.com/${owner}/${repo}/stargazers`,
    },
    watchers: {
      label: "👁️ Watchers",
      value: String(watchers),
      link: `https://github.com/${owner}/${repo}/watchers`,
    },
    forks: {
      label: "🍴 Forks",
      value: String(forks),
      link: `https://github.com/${owner}/${repo}/network/members`,
    },
    activity: {
      label: "📅 Activity",
      value: "View",
      link: `https://github.com/${owner}/${repo}/activity`,
    },
  };

  const markdown = `### 📊 Repository Statistics

[![Stars](${shieldUrl(badges.stars.label, badges.stars.value, "blue")})](${badges.stars.link})
[![Watchers](${shieldUrl(badges.watchers.label, badges.watchers.value, "blue")})](${badges.watchers.link})
[![Forks](${shieldUrl(badges.forks.label, badges.forks.value, "blue")})](${badges.forks.link})
[![Activity](${shieldUrl(badges.activity.label, badges.activity.value, "informational")})](${badges.activity.link})

**Last Updated:** ${pushedAt}

---
`;
  return markdown;
}

function updateReadme(readmePath, badgesMarkdown, owner, repo) {
  try {
    let content = fs.readFileSync(readmePath, "utf-8");

    const pattern = /### 📊 Repository Statistics\n\n.*?\n---\n/s;

    if (pattern.test(content)) {
      content = content.replace(pattern, badgesMarkdown);
    } else {
      const titlePattern = /(# [^\n]+\n)/;
      if (titlePattern.test(content)) {
        content = content.replace(titlePattern, `$1\n${badgesMarkdown}\n`);
      } else {
        content = badgesMarkdown + "\n" + content;
      }
    }

    fs.writeFileSync(readmePath, content, "utf-8");
    return true;
  } catch (e) {
    console.error(`Error updating README.md: ${e.message}`);
    return false;
  }
}

async function main() {
  const owner = "Logiclayer1111";
  const repo = "minGPT";
  const readmePath = path.join(__dirname, "README.md");

  try {
    console.log(`Fetching repository data for ${owner}/${repo}...`);
    const data = await fetchRepoData(owner, repo, process.env.GITHUB_TOKEN);

    console.log(`[+] Stars: ${data.stargazers_count || 0}`);
    console.log(`[+] Watchers: ${data.watchers_count || 0}`);
    console.log(`[+] Forks: ${data.forks_count || 0}`);

    const badgesMarkdown = generateBadgeMarkdown(owner, repo, data);

    if (updateReadme(readmePath, badgesMarkdown, owner, repo)) {
      console.log("[+] Updated README.md with live badges");
      return 0;
    } else {
      console.error("Failed to update README.md");
      return 1;
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    return 1;
  }
}

main().then((code) => process.exit(code));
