import mdtoc


def test_slugify_basic():
    assert mdtoc.slugify("Hello World") == "hello-world"

def test_slugify_strips_punctuation():
    assert mdtoc.slugify("What's new?") == "whats-new"
