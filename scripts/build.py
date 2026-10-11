#!/usr/bin/env python3
"""Validate data/*.yaml, refresh GitHub stats, and generate README.md.

Usage:
  python3 scripts/build.py            # refresh stats from GitHub, write README
  python3 scripts/build.py --offline  # reuse data/stats.json, write README
  python3 scripts/build.py --check    # validate only; exit 1 on any error
  python3 scripts/build.py --next-dex # print the dex number for a new entry

Needs GITHUB_TOKEN in the environment (or a logged-in `gh`) to refresh stats.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STATS = DATA / "stats.json"
README = ROOT / "README.md"

# Section order on the page. A data file not listed here fails validation,
# so a new category is a deliberate edit rather than an accident.
SECTIONS = ["coding-agents", "app-builders", "mcp", "agent-frameworks", "agent-infra", "local-models"]

RETIRED = json.loads((DATA / "retired.json").read_text())  # dex numbers of removed tools
STALE_DAYS = 180
MAX_DESC = 100
# Dex numbers are permanent IDs, like a Pokedex. They are never reused or
# renumbered, so a removed tool leaves a gap rather than shifting the rest.
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def load_sections():
    files = {p.stem for p in DATA.glob("*.yaml")}
    unknown = files - set(SECTIONS)
    if unknown:
        sys.exit(f"error: data files not in SECTIONS: {sorted(unknown)}")
    return [(name, yaml.safe_load((DATA / f"{name}.yaml").read_text())) for name in SECTIONS]


def validate(sections):
    errors, names, repos, dexes = [], {}, {}, {}
    for file, sec in sections:
        for key in ("title", "blurb", "groups"):
            if key not in sec:
                errors.append(f"{file}: missing '{key}'")
        for group in sec.get("groups", []):
            for t in group.get("tools", []):
                where = f"{file} > {group.get('title')} > {t.get('name', '?')}"
                for key in ("name", "url", "description"):
                    if not t.get(key):
                        errors.append(f"{where}: missing '{key}'")
                if not str(t.get("url", "")).startswith("https://"):
                    errors.append(f"{where}: url must be https")
                desc = t.get("description", "")
                if len(desc) > MAX_DESC:
                    errors.append(f"{where}: description is {len(desc)} chars (max {MAX_DESC})")
                if desc and not desc.endswith("."):
                    errors.append(f"{where}: description must end with a period")
                if t.get("repo") and not REPO_RE.match(t["repo"]):
                    errors.append(f"{where}: repo must be 'owner/name'")
                dex = t.get("dex")
                if not isinstance(dex, int) or dex < 1:
                    errors.append(f"{where}: needs a positive integer 'dex' (run --next-dex)")
                elif dex in RETIRED:
                    errors.append(f"{where}: dex {dex} is retired and can't be reused (run --next-dex)")
                elif dex in dexes:
                    errors.append(f"{where}: dex {dex} already used by {dexes[dex]}")
                else:
                    dexes[dex] = where
                n = t.get("name", "").lower()
                if n in names:
                    errors.append(f"{where}: duplicate name (also in {names[n]})")
                names[n] = where
                if t.get("repo"):
                    r = t["repo"].lower()
                    if r in repos:
                        errors.append(f"{where}: duplicate repo (also in {repos[r]})")
                    repos[r] = where
    return errors


def next_dex(sections):
    used = [t.get("dex", 0) for _, sec in sections for g in sec["groups"] for t in g["tools"]]
    return max(used + RETIRED + [0]) + 1


def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def fetch_repo(repo, tok):
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}")
    req.add_header("Accept", "application/vnd.github+json")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
            break
        except urllib.error.HTTPError as e:
            return {"error": e.code}
        except (urllib.error.URLError, TimeoutError):  # flaky network: retry, then give up
            if attempt == 2:
                return {"error": "network"}
    lic = (d.get("license") or {}).get("spdx_id")
    return {
        "full_name": d["full_name"],
        "stars": d["stargazers_count"],
        "pushed_at": d["pushed_at"],
        "archived": d["archived"],
        "license": None if lic in (None, "NOASSERTION") else lic,
    }


def refresh_stats(sections):
    tok = token()
    cached = json.loads(STATS.read_text()) if STATS.exists() else {}
    stats, problems = {}, []
    for _, sec in sections:
        for group in sec["groups"]:
            for t in group["tools"]:
                if not t.get("repo"):
                    continue
                s = fetch_repo(t["repo"], tok)
                if "error" in s:
                    problems.append(f"{t['name']}: {t['repo']} returned {s['error']}; keeping cached stats")
                    if t["repo"] in cached:
                        stats[t["repo"]] = cached[t["repo"]]
                    continue
                if not s["license"] and not t.get("license"):
                    problems.append(f"{t['name']}: GitHub can't classify the license; add a 'license:' override")
                if s["full_name"].lower() != t["repo"].lower():
                    problems.append(f"{t['name']}: {t['repo']} moved to {s['full_name']}")
                stats[t["repo"]] = s
    STATS.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n")
    return stats, problems


def human_stars(n):
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def age_label(pushed_at, today):
    days = (today - dt.date.fromisoformat(pushed_at[:10])).days
    if days <= 1:
        return "today"
    if days < 30:
        return f"{days}d ago"
    if days < 365:
        return f"{days // 30}mo ago"
    return f"{days // 365}y ago"


def anchor(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def row(t, stats, today):
    s = stats.get(t.get("repo"))
    num = f"#{t['dex']:03d}"
    name = f"[{t['name']}]({t['url']})"
    if t.get("maintainer_note"):
        name += " ¹"
    if not s and t.get("repo"):  # open source, but stats not fetched yet (--offline)
        return f"| {num} | {name} | {t['description']} | {t.get('license', '—')} | [★ ?](https://github.com/{t['repo']}) | — |", 0
    if not s:
        return f"| {num} | {name} | {t['description']} | Closed source | — | — |", -1
    flags = []
    if s["archived"]:
        flags.append("🗄️ archived")
    elif (today - dt.date.fromisoformat(s["pushed_at"][:10])).days > STALE_DAYS:
        flags.append("💤 stale")
    stars = f"[★ {human_stars(s['stars'])}](https://github.com/{s['full_name']})"
    activity = age_label(s["pushed_at"], today) + ("".join(f" · {f}" for f in flags))
    lic = t.get("license") or s["license"] or "Other"
    return f"| {num} | {name} | {t['description']} | {lic} | {stars} | {activity} |", s["stars"]


def render(sections, stats, today):
    sections = [(f, sec) for f, sec in sections if sec["groups"]]  # skip sections not seeded yet
    total = sum(len(g["tools"]) for _, sec in sections for g in sec["groups"])
    out = [
        "# AI Tools Index",
        "",
        "A maintained index of the AI tools developers actually use: coding agents, app builders, "
        "MCP servers, and the infrastructure underneath them.",
        "",
        "Unlike most lists, every entry is structured data. Stars, last activity and license are "
        "refreshed from GitHub nightly, and archived or inactive projects are flagged automatically "
        "instead of rotting in place. Each tool gets a permanent dex number, Pokédex-style, that "
        "never changes or gets reused.",
        "",
        f"**{total} tools** · updated {today.isoformat()} · "
        "[contribute](CONTRIBUTING.md)",
        "",
        "## Contents",
        "",
    ]
    for _, sec in sections:
        out.append(f"- [{sec['title']}](#{anchor(sec['title'])})")
        for g in sec["groups"]:
            out.append(f"  - [{g['title']}](#{anchor(g['title'])})")
    for _, sec in sections:
        out += ["", f"## {sec['title']}", "", sec["blurb"]]
        for g in sec["groups"]:
            rows = [row(t, stats, today) for t in g["tools"]]
            # Open source by stars, then closed source in data-file order.
            rows.sort(key=lambda r: -r[1] if r[1] >= 0 else float("inf"))
            out += [
                "",
                f"### {g['title']}",
                "",
                "| # | Tool | What it does | License | Stars | Last commit |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
            out += [r for r, _ in rows]
    out += [
        "",
        "---",
        "",
        f"💤 stale: no commits in {STALE_DAYS} days. 🗄️ archived: read-only on GitHub. "
        "\"+ enterprise\" / \"+ pro\": open core, with some directories under a commercial license.",
        "",
        "¹ Built by [Ergonlabs](https://ergonlabs.io), which maintains this list. "
        "It is held to the same inclusion rules as every other entry.",
        "",
        "Generated by `scripts/build.py` from [`data/`](data/). Edit the YAML, not this file.",
        "",
    ]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="reuse data/stats.json")
    ap.add_argument("--check", action="store_true", help="validate data only")
    ap.add_argument("--next-dex", action="store_true", help="print the next free dex number")
    args = ap.parse_args()

    sections = load_sections()
    if args.next_dex:
        print(next_dex(sections))
        return
    errors = validate(sections)
    if errors:
        print("\n".join(f"error: {e}" for e in errors), file=sys.stderr)
        sys.exit(1)
    if args.check:
        print("data OK")
        return

    problems = []
    if args.offline:
        stats = json.loads(STATS.read_text()) if STATS.exists() else {}
    else:
        stats, problems = refresh_stats(sections)
    README.write_text(render(sections, stats, dt.date.today()))
    for p in problems:
        print(f"warning: {p}", file=sys.stderr)
    print(f"wrote {README.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
