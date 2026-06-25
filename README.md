# mdtoc

> Generate or refresh a table of contents in a Markdown file, in place, with GitHub-compatible anchors.

## Why

Long READMEs need a table of contents, and a hand-maintained one is wrong
within a week. `mdtoc` regenerates it from the headings, in place, and can fail
CI when someone forgets.

## Usage

```
python mdtoc.py README.md              # print the TOC
python mdtoc.py README.md --write      # edit the file in place
python mdtoc.py README.md --check      # exit 1 if out of date
python mdtoc.py docs/guide.md --max-level 3 --write
```

## Markers

The generated block lives between two HTML comments, so the rest of the file is
never touched:

```markdown
<!-- mdtoc -->
- [Install](#install)
- [Usage](#usage)
  - [Flags](#flags)
<!-- /mdtoc -->
```

If the markers are absent, the block is inserted just after the `# Title` line
on the first run.
