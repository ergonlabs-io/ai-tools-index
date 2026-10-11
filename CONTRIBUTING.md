# Contributing

Every entry lives in a YAML file in [`data/`](data/). `README.md` is generated from those files, so
edit the YAML and leave the README alone; CI rebuilds it.

## Adding a tool

Add an entry to the right group in the right file:

```yaml
- name: Example
  dex: 50                     # from: python3 scripts/build.py --next-dex
  url: https://example.com
  repo: example-org/example   # optional; only for public GitHub repos
  description: One plain sentence on what it does, under 100 characters.
  added: 2026-10-20           # today's date; shows 🆕 for 30 days
```

Then check your entry locally:

```bash
pip install pyyaml
python3 scripts/build.py --check
```

## What gets in

- **It's real and available.** Publicly usable for at least 30 days. No waitlists, no announcements.
- **It's for developers building with AI.** Coding agents, app builders, MCP servers and the
  infrastructure that runs agents. General AI apps (chatbots, image generators) belong elsewhere.
- **The description is a fact, not a pitch.** Say what it does. "Best", "revolutionary",
  "game-changing" and "#1" get the PR sent back.
- **One tool per PR**, so each one can be reviewed on its own.
- **Disclose affiliation.** Adding your own tool is fine; tick the box in the PR template.

## What gets out

Nothing is removed for being unpopular. Stars and activity are shown so readers can judge
for themselves. A project is removed (and its dex number retired) when its links are dead, or when it has been archived
for 6 months and something better maintained does the same job.

## Dex numbers

Every tool has a permanent number, like a Pokédex. Take the next free one with
`python3 scripts/build.py --next-dex`. Numbers are never changed or reused: when a tool is
removed, its number goes into `data/retired.json`, and CI rejects any entry that tries to take it.

## License override

If the README shows the wrong license (GitHub reports custom or dual licenses as unknown), add
`license:` to the entry with the real one, e.g. `license: MIT + enterprise`.

## Markers

Add `hosted: true` to a tool that only runs as a hosted service (a website or cloud product you
can't install). New entries also get `added:` with today's date, which shows 🆕 for 30 days.

## Badge

If your tool is listed, you can add this to its README:

```markdown
[![Listed in AI Tools Index](https://img.shields.io/badge/Listed_in-AI_Tools_Index-0b7285)](https://github.com/ergonlabs-io/ai-tools-index)
```
