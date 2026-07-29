from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text()


def test_responsive_assets_include_intermediate_portrait_and_compact_logo():
    portrait = ROOT / "assets" / "portrait-alexandre-lasly-720.webp"
    logo = ROOT / "assets" / "atlas-nexus-logo-96.webp"

    assert portrait.exists()
    assert logo.exists()
    assert "portrait-alexandre-lasly-720.webp 720w" in HTML
    assert 'src="assets/atlas-nexus-logo-96.webp?v=1"' in HTML
