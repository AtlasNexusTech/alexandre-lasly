from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


def test_recruiter_facing_hero_is_specific_and_actionable():
    assert "Account Manager / Customer Success B2B" in HTML
    assert "8 ans d’expérience" in HTML
    assert 'href="https://www.linkedin.com/in/alexandre-lasly"' in HTML
    assert 'href="#contact"' in HTML


def test_person_schema_uses_verified_public_profiles():
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S)
    assert match is not None
    data = json.loads(match.group(1))
    assert data["@type"] == "Person"
    assert data["jobTitle"] == "Account Manager / Customer Success B2B"
    assert "https://www.linkedin.com/in/alexandre-lasly" in data["sameAs"]
    assert "https://github.com/AtlasNexusTech" in data["sameAs"]


def test_ambiguous_or_abstract_copy_is_replaced():
    assert "107 devis détaillés traités en une heure" not in HTML
    assert "4 références internationales citées" not in HTML
    assert "intelligences computationnelles" not in HTML
    assert "Ventes conclues notamment pour ITER, l’OCDE" in HTML
    assert "outils numériques, l’automatisation et l’IA" in HTML


if __name__ == "__main__":
    tests = [(name, value) for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for name, test in tests:
        test()
        print(f"PASS {name}")
