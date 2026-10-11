#!/usr/bin/env python3
"""Check a batch of proposed entries, one by one.

Every claim in a batch is checked against GitHub and the live web: repos that
don't exist or were renamed, dead or redirected sites, stale projects, marketing
copy, duplicates. Passing entries go to <batch>.verified.yaml; the reasons for
every rejection go to <batch>.report.md.

Usage: python3 scripts/verify.py staging/<batch>.yaml
"""
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402  (reuses SECTIONS, validation constants, token)

MIN_STARS = 200
MAX_IDLE_DAYS = 365
BANNED = re.compile(
    r"\b(best|leading|revolutionary|game[- ]chang\w*|cutting[- ]edge|powerful|seamless\w*|"
    r"supercharge\w*|unleash\w*|blazing\w*|world[- ]class|#1|ultimate|effortless\w*|"
    r"next[- ]gen\w*|state[- ]of[- ]the[- ]art|user[- ]friendly|easy|easily|we|our|you)\b",
    re.I,
)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15"
ALLOWED_FIELDS = {"section", "group", "name", "url", "repo", "hosted", "description", "evidence"}


def existing_index():
    names, repos, hosts = {}, {}, {}
    for file, sec in build.load_sections():
        for g in sec["groups"]:
            for t in g["tools"]:
                names[t["name"].lower()] = t["name"]
                if t.get("repo"):
                    repos[t["repo"].lower()] = t["name"]
                if "github.com" not in t["url"]:
                    hosts[urlparse(t["url"]).netloc.removeprefix("www.")] = t["name"]
    return names, repos, hosts


def fetch_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.geturl(), r.read(200_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # DNS failure, TLS error, timeout
        return None, url, str(e)


def name_on_page(name, html):
    # The tool's name (or its longest word) should appear somewhere on its own site.
    text = html.lower()
    words = sorted(re.findall(r"[a-z0-9]+", name.lower()), key=len, reverse=True)
    return name.lower() in text or (words and words[0] in text)


def check(entry, idx, tok, today):
    """Return (problems, notes, fixed_entry). Any problem rejects the entry."""
    problems, notes = [], []
    e = dict(entry)
    names, repos, hosts = idx

    for key in ("section", "group", "name", "url", "description", "evidence"):
        if not e.get(key):
            problems.append(f"missing '{key}'")
    extra = set(e) - ALLOWED_FIELDS
    if extra:
        problems.append(f"unknown fields {sorted(extra)}")
    if problems:
        return problems, notes, e

    if e["section"] not in build.SECTIONS:
        problems.append(f"section must be one of {build.SECTIONS}")
    d = e["description"].strip()
    if len(d) > build.MAX_DESC:
        problems.append(f"description is {len(d)} chars; max {build.MAX_DESC}")
    if not d.endswith("."):
        problems.append("description must end with a period")
    m = BANNED.search(d)
    if m:
        problems.append(f"description uses marketing/first-person word '{m.group(0)}'; state a plain fact")
    first = re.split(r"[\s,]", d, maxsplit=1)[0].lower()
    if d.lower().startswith(e["name"].lower()) or first in {"a", "an", "the"}:
        problems.append("description must start with a verb (e.g. 'Runs ...'), not the tool's name or an article")
    if not e["url"].startswith("https://"):
        problems.append("url must start with https://")
    if e["name"].lower() in names:
        problems.append(f"duplicate: already listed as '{names[e['name'].lower()]}'")

    if e.get("repo"):
        if not build.REPO_RE.match(e["repo"]):
            problems.append("repo must be 'owner/name' with no URL")
        else:
            s = build.fetch_repo(e["repo"], tok)
            if "error" in s:
                problems.append(f"GitHub repo {e['repo']} does not exist (HTTP {s['error']}); find the real one or drop 'repo'")
            else:
                if s["full_name"].lower() != e["repo"].lower():
                    notes.append(f"repo renamed {e['repo']} -> {s['full_name']}; fixed")
                    e["repo"] = s["full_name"]
                if s["full_name"].lower() in repos:
                    problems.append(f"duplicate: repo already listed as '{repos[s['full_name'].lower()]}'")
                if s["archived"]:
                    problems.append("repo is archived; drop this tool")
                idle = (today - build.dt.date.fromisoformat(s["pushed_at"][:10])).days
                if idle > MAX_IDLE_DAYS:
                    problems.append(f"no commits in {idle} days; drop this tool")
                if s["stars"] < MIN_STARS:
                    problems.append(f"only {s['stars']} stars (min {MIN_STARS}); drop this tool")
                if not s["license"] and not e.get("license"):
                    notes.append("GitHub can't classify the license; needs a manual 'license:' override")

    host = urlparse(e["url"]).netloc.removeprefix("www.")
    if host in hosts and "github.com" not in host:
        problems.append(f"duplicate: {host} already listed as '{hosts[host]}'")
    status, final, html = fetch_page(e["url"])
    if status is None:
        problems.append(f"url does not load ({html[:80]})")
    elif status in (403, 429):
        notes.append(f"url returned {status} (bot-blocked); assumed alive, check by hand")
    elif status >= 400:
        problems.append(f"url returned HTTP {status}")
    else:
        fhost = urlparse(final).netloc.removeprefix("www.")
        if fhost != host:
            problems.append(f"url redirects to another site ({final}); the tool may have been renamed or acquired")
        elif not e.get("repo") and not name_on_page(e["name"], html):
            problems.append(f"'{e['name']}' does not appear on {e['url']}; is this the right site?")
    return problems, notes, e


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    try:
        entries = yaml.safe_load(path.read_text()) or []
    except yaml.YAMLError as err:
        path.with_suffix(".report.md").write_text(f"# Verify report\n\nThe file is not valid YAML:\n\n```\n{err}\n```\n")
        sys.exit(f"invalid YAML: {err}")
    if not isinstance(entries, list):
        sys.exit("batch must be a YAML list of entries")

    idx, tok, today = existing_index(), build.token(), build.dt.date.today()
    passed, report, seen = [], [], set()
    for entry in entries:
        name = (entry or {}).get("name", "?")
        if name.lower() in seen:
            report.append(f"## REJECT {name}\n- listed twice in this batch\n")
            continue
        seen.add(name.lower())
        problems, notes, fixed = check(entry or {}, idx, tok, today)
        if problems:
            report.append(f"## REJECT {name}\n" + "".join(f"- {p}\n" for p in problems + notes))
        else:
            fixed.pop("evidence", None)
            passed.append(fixed)
            report.append(f"## PASS {name}\n" + "".join(f"- note: {n}\n" for n in notes))

    out = path.with_name(path.stem + ".verified.yaml")
    out.write_text(yaml.safe_dump(passed, sort_keys=False, allow_unicode=True))
    rejected = len(entries) - len(passed)
    summary = f"{len(passed)} passed, {rejected} rejected of {len(entries)}"
    path.with_name(path.stem + ".report.md").write_text(f"# Verify report: {summary}\n\n" + "\n".join(report))
    print(summary)
    print(json.dumps({"passed": len(passed), "rejected": rejected}))


if __name__ == "__main__":
    main()
