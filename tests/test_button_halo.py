import re
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from html.parser import HTMLParser
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text()
CSS = (ROOT / "styles.css").read_text()
MOTION = (ROOT / "src" / "motion.js").read_text()


class ButtonParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        node = {"tag": tag, "attrs": attrs, "text": ""}
        if tag in {"a", "button"} and "button" in (attrs.get("class") or "").split():
            self.buttons.append(node)
        self.stack.append(node)

    def handle_data(self, data):
        for node in self.stack:
            node["text"] += data

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break


class ButtonHaloContract(unittest.TestCase):
    def test_only_requested_contact_buttons_opt_out_of_halo(self):
        parser = ButtonParser()
        parser.feed(HTML)
        targets = {
            " ".join(node["text"].split()): node
            for node in parser.buttons
            if " ".join(node["text"].split()) in {
                "Me contacter",
                "Afficher mes coordonnées →",
            }
        }
        self.assertEqual(set(targets), {"Me contacter", "Afficher mes coordonnées →"})
        for node in targets.values():
            self.assertIn("data-no-halo", node["attrs"])

        other_buttons = [node for node in parser.buttons if node not in targets.values()]
        self.assertTrue(other_buttons)
        self.assertTrue(all("data-no-halo" not in node["attrs"] for node in other_buttons))

    def test_motion_and_css_honor_the_opt_out(self):
        self.assertIn(".button:not([data-no-halo])", MOTION)
        self.assertRegex(
            CSS,
            re.compile(r"\.button\[data-no-halo\][^{]*\{[^}]*box-shadow:\s*none", re.S),
        )
        self.assertRegex(
            CSS,
            re.compile(r"\.button\[data-no-halo\]:hover[^{]*\{[^}]*box-shadow:\s*none", re.S),
        )


@pytest.fixture()
def portfolio_url():
    handler = partial(SimpleHTTPRequestHandler, directory=ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/?button-halo-regression=1"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.mark.parametrize("viewport", [{"width": 1280, "height": 900}, {"width": 390, "height": 844}])
def test_requested_contact_buttons_render_without_halo(portfolio_url, viewport):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport=viewport)
        page.goto(portfolio_url, wait_until="networkidle")

        contact_link = page.get_by_role("link", name="Me contacter", exact=True)
        reveal_button = page.get_by_role("button", name="Afficher mes coordonnées", exact=True)
        primary_cta = page.get_by_role("link", name="Découvrir mon parcours", exact=False)

        for target in (contact_link, reveal_button):
            assert target.locator(".button-pulse-ring").count() == 0
            assert target.evaluate("element => getComputedStyle(element).boxShadow") == "none"

        assert primary_cta.locator(".button-pulse-ring").count() == 1

        reveal_button.click()
        reveal_control = page.locator("[data-contact-reveal]")
        assert reveal_control.get_attribute("aria-expanded") == "true"
        assert page.locator("#coordonnees a").count() == 2
        browser.close()


if __name__ == "__main__":
    unittest.main()
