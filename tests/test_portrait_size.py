from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "styles.css").read_text()
HTML = (ROOT / "index.html").read_text()


def test_profile_portrait_is_compact_and_centered():
    portrait_rule = CSS.split(".profile-portrait {", 1)[1].split("}", 1)[0]
    assert "width: calc(100% - 48px);" in portrait_rule
    assert "max-width: 320px;" in portrait_rule
    assert "margin: 28px auto 0;" in portrait_rule
    assert "border-radius:" in portrait_rule


def test_portrait_stylesheet_cache_is_versioned():
    assert 'styles.css?v=portrait2' in HTML
