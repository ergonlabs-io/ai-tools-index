#!/usr/bin/env python3
"""Turn a brief of candidate tools into draft entries, using a free model with no tools.

The script does all the fact-finding (GitHub search, the homepage's title and meta
description) and hands the model those facts. The model only chooses among them and
writes one sentence per tool. It runs in a fresh temp directory outside the repo with
every opencode tool disabled and every permission denied (passed inline, so no project
config can override it), and the repo is checked for stray files after every call. Any repo or URL in its answer
that wasn't in the facts it was given is dropped before verify.py ever sees it.

Usage: python3 scripts/research.py <batch> pipeline/briefs/<batch>.yaml
Then:  read staging/<batch>.verified.yaml, and python3 scripts/merge.py it.

Env: MODELS (comma-separated, tried in order), TIMEOUT per call in seconds (default 300).
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import verify  # noqa: E402

ROOT = build.ROOT
# Inline config: every tool off and every permission denied. A config file in a directory
# was not enough: opencode resolved its project elsewhere and the model wrote files.
LOCKDOWN = json.dumps({
    "permission": "deny",
    "tools": {t: False for t in ["bash", "edit", "write", "patch", "read", "glob", "grep", "list", "lsp",
                                 "webfetch", "websearch", "task", "todowrite", "todoread", "skill", "question"]},
})
STAGING = ROOT / "staging"
LOGS = ROOT / "logs"
OPENCODE = os.environ.get("OPENCODE") or str(Path.home() / ".opencode/bin/opencode")
MODELS = os.environ.get("MODELS", "openrouter/nvidia/nemotron-3-super-120b-a12b:free,"
                        "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free,"
                        "openrouter/google/gemma-4-31b-it:free").split(",")
TIMEOUT = int(os.environ.get("TIMEOUT", "300"))
CHUNK = 6  # candidates per model call; small prompts keep weak models on task


def gh_search(name, tok):
    q = urllib.parse.quote(f"{name} in:name")
    req = urllib.request.Request(f"https://api.github.com/search/repositories?q={q}&sort=stars&per_page=3",
                                 headers={"Accept": "application/vnd.github+json",
                                          **({"Authorization": f"Bearer {tok}"} if tok else {})})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            items = json.load(r)["items"]
    except Exception:
        return []
    return [{"repo": i["full_name"], "stars": i["stargazers_count"], "description": i["description"],
             "homepage": i["homepage"] or None, "archived": i["archived"], "last_commit": i["pushed_at"][:10]}
            for i in items]


def page_facts(url):
    status, final, body = verify.fetch_page(url)
    if not status or status >= 400:
        return {"url": url, "loads": False, "http_status": status}
    def meta(prop):
        m = re.search(rf'<meta[^>]+(?:name|property)=["\']{prop}["\'][^>]+content=["\']([^"\']+)', body, re.I) or \
            re.search(rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:name|property)=["\']{prop}["\']', body, re.I)
        return html.unescape(m.group(1)).strip() if m else None
    t = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    return {"url": final, "loads": True, "title": html.unescape(t.group(1)).strip()[:150] if t else None,
            "description": (meta("description") or meta("og:description") or "")[:300] or None}


def gather(c, tok):
    """Facts for one candidate, plus the only repos and URLs the model may use."""
    facts = {"candidate": c.get("name") or c.get("hint"), "group_hint": c.get("group")}
    repos = []
    url = c.get("url")
    if url and urllib.parse.urlparse(url).netloc == "github.com":
        parts = urllib.parse.urlparse(url).path.strip("/").split("/")
        if len(parts) >= 2:
            s = build.fetch_repo("/".join(parts[:2]), tok)
            if "error" not in s:
                repos.append({"repo": s["full_name"], "stars": s["stars"], "archived": s["archived"],
                              "last_commit": s["pushed_at"][:10]})
    if c.get("name"):
        repos += [r for r in gh_search(c["name"], tok) if r["repo"] not in {x["repo"] for x in repos}]
    facts["github_repos"] = repos[:4]
    sites = [u for u in [url] + [r.get("homepage") for r in repos[:2]] if u and u.startswith("https://")]
    facts["websites"] = [page_facts(u) for u in dict.fromkeys(sites)]
    allowed_urls = {u for u in sites} | {w["url"] for w in facts["websites"]} | {f"https://github.com/{r['repo']}" for r in repos}
    return facts, {r["repo"].lower() for r in repos}, {u.rstrip("/").lower() for u in allowed_urls}


PROMPT = """You turn research facts into entries for an index of AI developer tools.
Use ONLY the facts below. Do not use outside knowledge for repos or URLs.

{instructions}

For each candidate, decide whether it is a real AI developer tool that fits a section in
[{sections}]. If it does not, or the facts are not enough, leave it out.

For each one you keep, output:
- section: one of the sections above
  group: {group_rule}
  name: the product's own name, as in the facts
  url: the official website from "websites" (prefer it), else https://github.com/<repo>
  repo: owner/name copied exactly from "github_repos" ONLY if it is clearly this tool's own repo; else omit
  description: one plain sentence under 100 characters ending with a period, saying what it does
  evidence: the exact text from the facts your description is based on

Description rules: plain facts only. Start with a verb and never with the tool's name:
"Runs open-weight LLMs locally behind an OpenAI-compatible API." not "Ollama is a tool that...".
Be specific about what it does; "An open source AI engine." says nothing. No marketing words
(best, powerful, seamless, leading, ultimate, revolutionary, user-friendly, easy).
No "you", "we", "our". Do not invent features or numbers.
Skip any tool whose repo is archived, has under 200 stars, or had no commit in a year.
{feedback}
Reply with only a YAML list in one ```yaml fenced block. An empty list [] is fine.

FACTS
{facts}
"""


def repo_files():
    return {p for p in ROOT.rglob("*") if p.is_file() and not p.is_relative_to(STAGING)
            and not p.is_relative_to(LOGS) and ".git" not in p.parts and "__pycache__" not in p.parts}


def call_model(prompt, tag):
    LOGS.mkdir(exist_ok=True)
    pfile = LOGS / f"{tag}.prompt.md"
    pfile.write_text(prompt)
    env = {**os.environ, "OPENCODE_CONFIG_CONTENT": LOCKDOWN, "OPENCODE_CONFIG_PROJECT_DISABLE": "1"}
    for model in MODELS:
        before = repo_files()
        with tempfile.TemporaryDirectory(prefix="aitools-model-") as cwd:
            try:
                p = subprocess.run([OPENCODE, "run", "--standalone", "-m", model, "-f", str(pfile),
                                    "The attached file is your full instructions. Follow it exactly."],
                                   cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT)
                out = p.stdout
            except subprocess.TimeoutExpired:
                out, p = "", None
        stray = repo_files() - before
        if stray:
            sys.exit(f"ABORT: the model created files in the repo despite the lockdown: {sorted(map(str, stray))}")
        (LOGS / f"{tag}.out.txt").write_text(out + "\n--- stderr ---\n" + (p.stderr if p else "timeout"))
        m = re.search(r"```(?:yaml)?\s*\n(.*?)```", out, re.S)
        if m:
            try:
                data = yaml.safe_load(m.group(1)) or []
                if isinstance(data, list):
                    print(f"  {tag}: {model.split('/')[-1]} -> {len(data)} entries")
                    return data
            except yaml.YAMLError:
                pass
        print(f"  {tag}: {model.split('/')[-1]} failed ({'timeout' if p is None else f'exit {p.returncode}'}); trying next")
    return []


def run_chunk(brief, chunk, tag, tok, feedback=""):
    gathered = [gather(c, tok) for c in chunk]
    group_rule = ("the candidate's group_hint if given; else an existing group name from that section, "
                  "or a short new one")
    prompt = PROMPT.format(instructions=brief.get("instructions", "").strip(),
                           sections=", ".join(build.SECTIONS), group_rule=group_rule, feedback=feedback,
                           facts=json.dumps([g[0] for g in gathered], indent=1, ensure_ascii=False))
    entries = call_model(prompt, tag)
    allowed_repos = set().union(*(g[1] for g in gathered)) if gathered else set()
    allowed_urls = set().union(*(g[2] for g in gathered)) if gathered else set()
    kept = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        if e.get("repo") and e["repo"].lower() not in allowed_repos:
            print(f"    dropped {e.get('name')}: repo {e['repo']} was not in the facts (invented)")
            continue
        if str(e.get("url", "")).rstrip("/").lower() not in allowed_urls:
            print(f"    dropped {e.get('name')}: url {e.get('url')} was not in the facts (invented)")
            continue
        if brief.get("section") and not e.get("section"):
            e["section"] = brief["section"]
        kept.append(e)
    return kept


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    batch, brief = sys.argv[1], yaml.safe_load(Path(sys.argv[2]).read_text())
    STAGING.mkdir(exist_ok=True)
    tok = build.token()
    cands = brief["candidates"]
    chunks = [cands[i:i + CHUNK] for i in range(0, len(cands), CHUNK)]
    print(f"[{batch}] {len(cands)} candidates in {len(chunks)} calls")
    draft = []
    for i, chunk in enumerate(chunks):
        draft += run_chunk(brief, chunk, f"{batch}.{i}", tok)
    out = STAGING / f"{batch}.yaml"
    out.write_text(yaml.safe_dump(draft, sort_keys=False, allow_unicode=True))
    subprocess.run([sys.executable, str(ROOT / "scripts/verify.py"), str(out)], check=True)

    # One retry for rejected entries, with the verifier's reasons.
    report = (STAGING / f"{batch}.report.md").read_text()
    rejected = re.findall(r"^## REJECT (.+)\n((?:- .+\n)+)", report, re.M)
    fixable = [(n, r) for n, r in rejected if "duplicate" not in r and "archived" not in r and "stars" not in r]
    if fixable:
        names = {n.lower() for n, _ in fixable}
        retry = [c for c in cands if (c.get("name") or "").lower() in names]
        if retry:
            fb = "\nA previous attempt was rejected by the verifier for these reasons; fix them:\n" + \
                 "".join(f"- {n}: {r.strip()}\n" for n, r in fixable)
            print(f"[{batch}] retrying {len(retry)} rejected")
            fixed = run_chunk(brief, retry, f"{batch}.retry", tok, fb)
            keep = [e for e in draft if (e.get("name") or "").lower() not in names]
            out.write_text(yaml.safe_dump(keep + fixed, sort_keys=False, allow_unicode=True))
            subprocess.run([sys.executable, str(ROOT / "scripts/verify.py"), str(out)], check=True)
    print(f"[{batch}] review staging/{batch}.verified.yaml, then: python3 scripts/merge.py staging/{batch}.verified.yaml")


if __name__ == "__main__":
    main()
