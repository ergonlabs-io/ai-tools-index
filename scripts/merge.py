#!/usr/bin/env python3
"""Merge a verified staging batch into data/, assigning dex numbers.

Usage: python3 scripts/merge.py staging/<batch>.verified.yaml

Entries are appended to their section and group (a new group is created at the
end of the section). Data files are rewritten in the same hand-written style
they started in, so diffs stay small and readable.
"""
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

FIELD_ORDER = ["name", "dex", "url", "repo", "license", "description", "maintainer_note"]


def scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    # Plain if YAML reads it back unchanged; otherwise a JSON string, which is valid YAML.
    try:
        if yaml.safe_load(f"k: {v}") == {"k": v}:
            return v
    except yaml.YAMLError:
        pass
    return json.dumps(v, ensure_ascii=False)


def dump_section(sec):
    lines = [f"title: {scalar(sec['title'])}", f"blurb: {scalar(sec['blurb'])}", "groups:"]
    for g in sec["groups"]:
        lines += [f"  - title: {scalar(g['title'])}", "    tools:"]
        for t in g["tools"]:
            keys = [k for k in FIELD_ORDER if k in t] + [k for k in t if k not in FIELD_ORDER]
            for i, k in enumerate(keys):
                lines.append(f"{'      - ' if i == 0 else '        '}{k}: {scalar(t[k])}")
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".verified.yaml"):
        sys.exit(__doc__)
    entries = yaml.safe_load(Path(sys.argv[1]).read_text()) or []
    sections = dict(build.load_sections())
    dex = build.next_dex(list(sections.items()))
    touched = set()
    for e in entries:
        sec = sections[e.pop("section")]
        gname = e.pop("group")
        group = next((g for g in sec["groups"] if g["title"].lower() == gname.lower()), None)
        if group is None:
            group = {"title": gname, "tools": []}
            sec["groups"].append(group)
        group["tools"].append({"dex": dex, **e})
        print(f"#{dex:03d} {e['name']} -> {sec['title']} / {group['title']}")
        dex += 1
        touched.add(next(k for k, v in sections.items() if v is sec))
    for name in touched:
        (build.DATA / f"{name}.yaml").write_text(dump_section(sections[name]))
    errors = build.validate(build.load_sections())
    if errors:
        sys.exit("merge produced invalid data:\n" + "\n".join(errors))
    print(f"merged {len(entries)} entries into {sorted(touched)}")


if __name__ == "__main__":
    main()
