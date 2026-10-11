#!/usr/bin/env python3
"""Find AI developer tools that are trending now, and write them up as a research brief.

No model runs here. This collects candidates from free, sanctioned sources, drops anything
already in data/ or already triaged, and writes pipeline/briefs/trends-<date>.md. That
brief goes through scripts/research.py like any other: a free model decides which candidates
fit a section and researches them, and verify.py checks every claim.

Sources:
  - Hacker News (Algolia API): stories and Show HNs from the last N days above a points bar.
  - GitHub search: repos created in the last 30 days, above a star bar, on AI topics.

Usage: python3 scripts/trendscan.py [--days 7] [--dry-run]
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

SEEN = build.ROOT / "pipeline" / "seen.json"  # candidates already triaged; never re-briefed
BRIEFS = build.ROOT / "pipeline" / "briefs"

HN_MIN_POINTS = 50
GH_MIN_STARS = 300
MAX_CANDIDATES = 25
HN_QUERIES = ["agent", "MCP", "LLM", "coding", "Claude", "Codex", "AI", "model", "vibe coding", "app builder"]
GH_TOPICS = ["ai-agents", "mcp", "mcp-server", "llm", "coding-agent", "claude-code", "agents", "ai-coding", "local-llm", "rag"]
# A candidate must look like an AI dev tool, not general AI news.
AI_WORDS = re.compile(r"\b(ai|llm|llms|agent|agents|agentic|mcp|claude|codex|gpt|gemini|model|models|copilot|rag|inference|prompt)\b", re.I)
SKIP_HOSTS = {"news.ycombinator.com", "twitter.com", "x.com", "youtube.com", "www.youtube.com", "arxiv.org",
              "medium.com", "substack.com", "nytimes.com", "theverge.com", "techcrunch.com", "bloomberg.com"}


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "ai-tools-index-trendscan", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def hacker_news(days):
    since = int(time.time()) - days * 86400
    found = {}
    for q in HN_QUERIES:
        params = urllib.parse.urlencode({
            "query": q,
            "tags": "story",
            "numericFilters": f"points>={HN_MIN_POINTS},created_at_i>{since}",
            "hitsPerPage": 50,
        })
        for h in get_json(f"https://hn.algolia.com/api/v1/search?{params}")["hits"]:
            url, title = h.get("url"), h.get("title") or ""
            if not url or urlparse(url).netloc in SKIP_HOSTS or not AI_WORDS.search(title):
                continue
            found[url] = {
                "title": title,
                "url": url,
                "signal": f"{h['points']} points on HN",
                "score": h["points"],
                "source": f"https://news.ycombinator.com/item?id={h['objectID']}",
            }
    return list(found.values())


def github_new(days_created=30):
    since = (build.dt.date.today() - build.dt.timedelta(days=days_created)).isoformat()
    tok = build.token()
    headers = {"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {tok}"} if tok else {})}
    found = {}
    for topic in GH_TOPICS:
        q = urllib.parse.quote(f"topic:{topic} created:>{since} stars:>={GH_MIN_STARS}")
        for r in get_json(f"https://api.github.com/search/repositories?q={q}&sort=stars&per_page=30", headers)["items"]:
            if r["archived"] or r["fork"]:
                continue
            found[r["full_name"]] = {
                "title": f"{r['full_name']}: {r['description'] or ''}"[:160],
                "url": r["html_url"],
                "repo": r["full_name"],
                "signal": f"{r['stargazers_count']} stars, created {r['created_at'][:10]}",
                "score": r["stargazers_count"] // 10,  # rough parity with HN points
                "source": r["html_url"],
            }
    return list(found.values())


def known():
    """Keys for everything already listed or already triaged."""
    keys = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    for _, sec in build.load_sections():
        for g in sec["groups"]:
            for t in g["tools"]:
                keys.add(t["name"].lower())
                keys.add(urlparse(t["url"]).netloc.removeprefix("www.") if "github.com" not in t["url"] else t["url"].lower())
                if t.get("repo"):
                    keys.add(t["repo"].lower())
    return keys


def key_of(c):
    if c.get("repo"):
        return c["repo"].lower()
    u = urlparse(c["url"])
    if u.netloc == "github.com":
        parts = u.path.strip("/").split("/")
        return "/".join(parts[:2]).lower() if len(parts) >= 2 else u.netloc
    return u.netloc.removeprefix("www.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="HN lookback window")
    ap.add_argument("--dry-run", action="store_true", help="print candidates; write nothing")
    args = ap.parse_args()

    seen = known()
    candidates, keys = [], set()
    for c in hacker_news(args.days) + github_new():
        k = key_of(c)
        if k in seen or k in keys:
            continue
        keys.add(k)
        candidates.append(c)
    candidates.sort(key=lambda c: -c["score"])
    candidates = candidates[:MAX_CANDIDATES]

    if args.dry_run or not candidates:
        for c in candidates:
            print(f"{c['score']:>5}  {c['title'][:90]}  ({c['signal']})")
        print(f"{len(candidates)} new candidates" + (" (dry run)" if args.dry_run else ""))
        return

    today = build.dt.date.today().isoformat()
    brief = {
        "instructions": (
            f"These trended on Hacker News or GitHub in the week to {today}. Many are NOT tools: news, "
            "essays, funding announcements, research papers, demos, games, toy projects. Keep only real, "
            "usable AI developer tools. Writing zero entries is fine."
        ),
        "candidates": [{"hint": f"{c['title']} ({c['signal']})", "url": c["url"]} for c in candidates],
    }
    out = BRIEFS / f"trends-{today}.yaml"
    out.write_text(yaml.safe_dump(brief, sort_keys=False, allow_unicode=True, width=120))
    # Mark as triaged now, so a candidate the model rejects isn't re-briefed every week.
    SEEN.write_text(json.dumps(sorted(set(json.loads(SEEN.read_text()) if SEEN.exists() else []) | keys), indent=0) + "\n")
    print(f"{len(candidates)} new candidates -> {out.relative_to(build.ROOT)}")


if __name__ == "__main__":
    main()
