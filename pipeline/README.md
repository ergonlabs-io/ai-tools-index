# Research pipeline

Bulk research runs on a free model with **no tools**. Scripts do all the fact-finding and
all the checking; the model only picks among facts it's handed and writes one sentence per
tool. The expensive model (or a human) only reads the final descriptions.

```
trendscan.py ──▶ briefs/trends-<date>.yaml ─┐
hand-written ──▶ briefs/<batch>.yaml ───────┤
                                            ▼
                 research.py: GitHub search + homepage title/description per candidate
                                            │
                 free model, temp dir, every tool off ──▶ YAML entries
                                            │
                 drop any repo/URL that wasn't in the facts (invented)
                                            │
                 verify.py ── rejects ──▶ one retry with reasons
                                            │
                 staging/<batch>.verified.yaml ──▶ read descriptions ──▶ merge.py ──▶ data/
```

## Commands

```bash
python3 scripts/trendscan.py --dry-run                         # what's trending, write nothing
python3 scripts/trendscan.py                                   # write briefs/trends-<date>.yaml
python3 scripts/research.py <batch> pipeline/briefs/<batch>.yaml
python3 scripts/merge.py staging/<batch>.verified.yaml         # after reading it
python3 scripts/build.py                                       # refresh stats + README
```

`MODELS` (comma-separated, tried in order) and `TIMEOUT` override the defaults in
`research.py`.

## Brief format

```yaml
section: local-models          # optional; omit to let the model choose (trend briefs)
instructions: One or two lines of context for the model.
candidates:
  - {name: Ollama, group: Runners, url: https://ollama.com}   # url needed for closed-source tools
  - {hint: "some-org/tool: what the repo says (900 stars)", url: https://github.com/some-org/tool}
```

## Why the model has no tools

- **Safety:** an autonomous model with a shell, running unattended, is a real risk.
  `research.py` runs each call in a fresh temp directory outside the repo, passes a config
  inline (`OPENCODE_CONFIG_CONTENT`) that disables every tool and denies every permission,
  ignores project configs, and aborts if the repo gains a file during the call. An earlier
  version used a config file in a sandbox directory; opencode didn't apply it and the model
  wrote its answers into the repo root. Tested by asking the model to write files and run
  shell commands: nothing was created (it still claimed it had).
- **Reliability:** the first version let the model run `gh` and browse. It hung for 15
  minutes and wrote nothing. Text in, text out finishes in seconds to minutes.
- **No invention:** the model can only use repos and URLs present in its facts; anything
  else is dropped in code before verification.

OpenCode's own `*-free` models refuse to run with tools disabled ("free tier can only be
used from within OpenCode"), so the defaults are OpenRouter free models, which use your
OpenRouter key. Free OpenRouter accounts are rate-limited per day; batches run sequentially.

## What verify.py rejects

Missing or unknown fields; a section that doesn't exist; descriptions over 100 characters,
without a final period, starting with the tool's name or an article, or using marketing or
first-person words; repos that don't exist, are archived, have no commits in a year, or have
under 200 stars; URLs that fail to load or redirect to another site (a sign of a rename or
acquisition); hosted sites that don't mention the tool's name; duplicates of an existing
entry by name, repo or domain. Renamed repos are fixed automatically.

What it can't check is whether a description is specific and true. That's the one manual
read before merging.
