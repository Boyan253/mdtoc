#!/usr/bin/env python3
"""Insert or update a table of contents in a Markdown document."""

import argparse
import re
import sys

__version__ = "0.1.0"

START = "<!-- mdtoc -->"
END = "<!-- /mdtoc -->"
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def slugify(text):
    """GitHub's heading anchor rules: lowercase, strip punctuation, spaces to dashes."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"[\s]+", "-", text)


def headings(text, min_level=2, max_level=4):
    """Yield (level, title, anchor) for every heading outside a code fence."""
    in_fence = False
    seen = {}
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if not match:
            continue
        level = len(match.group(1))
        if not min_level <= level <= max_level:
            continue
        title = match.group(2).strip()
        anchor = slugify(title)
        count = seen.get(anchor, 0)
        seen[anchor] = count + 1
        if count:
            anchor = "%s-%d" % (anchor, count)
        yield (level, title, anchor)


def build_toc(items, indent="  "):
    if not items:
        return ""
    base = min(level for level, _, _ in items)
    lines = []
    for level, title, anchor in items:
        lines.append("%s- [%s](#%s)" % (indent * (level - base), title, anchor))
    return "\n".join(lines)


def splice(text, toc):
    """Replace the block between the markers, or insert one after the title."""
    block = "%s\n%s\n%s" % (START, toc, END)
    if START in text and END in text:
        head, _, rest = text.partition(START)
        _, _, tail = rest.partition(END)
        return head + block + tail
    lines = text.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break
    lines.insert(insert_at, "\n" + block + "\n")
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("markdown_file")
    ap.add_argument("--min-level", type=int, default=2)
    ap.add_argument("--max-level", type=int, default=4)
    ap.add_argument("--write", action="store_true", help="edit the file in place")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the file is out of date (for CI)")
    args = ap.parse_args(argv)

    with open(args.markdown_file, encoding="utf-8") as fh:
        text = fh.read()
    toc = build_toc(list(headings(text, args.min_level, args.max_level)))
    updated = splice(text, toc)

    if args.check:
        if updated != text:
            print("mdtoc: table of contents is out of date", file=sys.stderr)
            return 1
        return 0
    if args.write:
        with open(args.markdown_file, "w", encoding="utf-8") as fh:
            fh.write(updated)
        print("updated %s" % args.markdown_file, file=sys.stderr)
    else:
        print(toc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
