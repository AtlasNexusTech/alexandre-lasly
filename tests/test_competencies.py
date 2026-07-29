from pathlib import Path


HTML = (Path(__file__).resolve().parents[1] / "index.html").read_text()


def test_competencies_use_current_terminology():
    expected = [
        "Outils numériques, données &amp; IA",
        "Microsoft 365",
        "Développement commercial",
        "Grands comptes &amp; contrats",
        "Relation client internationale",
        "Coordination de projet",
        "Anglais professionnel",
        "IA agentique &amp; veille",
    ]
    for text in expected:
        assert text in HTML

    outdated = ["Pack Office", "CRM · Data · Office", "Digital &amp; IA agentique"]
    for text in outdated:
        assert text not in HTML
