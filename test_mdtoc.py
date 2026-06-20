import mdtoc


def test_slugify_basic():
    assert mdtoc.slugify("Hello World") == "hello-world"

def test_slugify_strips_punctuation():
    assert mdtoc.slugify("What's new?") == "whats-new"


def test_slugify_keeps_dashes():
    assert mdtoc.slugify("Set-up guide") == "set-up-guide"

def test_headings_respects_levels():
    text = "# One\n## Two\n### Three\n"
    found = [t for _, t, _ in mdtoc.headings(text, 2, 2)]
    assert found == ["Two"]


def test_headings_ignores_code_fences():
    text = "## Real\n```\n## Not a heading\n```\n"
    assert [t for _, t, _ in mdtoc.headings(text)] == ["Real"]

def test_duplicate_headings_get_numbered_anchors():
    text = "## Setup\n## Setup\n"
    anchors = [a for _, _, a in mdtoc.headings(text)]
    assert anchors == ["setup", "setup-1"]
