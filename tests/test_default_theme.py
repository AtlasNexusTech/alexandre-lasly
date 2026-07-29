from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def portfolio_url():
    handler = partial(SimpleHTTPRequestHandler, directory=ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_dark_theme_is_default_even_when_system_prefers_light(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(color_scheme="light")
        page = context.new_page()
        page.goto(portfolio_url, wait_until="networkidle")

        assert page.locator("html").get_attribute("data-theme") == "dark"
        assert page.locator("[data-theme-toggle]").get_attribute("aria-label") == "Utiliser le thème clair"

        browser.close()


def test_dark_theme_is_applied_before_external_javascript(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(color_scheme="light")
        page = context.new_page()
        page.route("**/script.js", lambda route: route.abort())
        page.goto(portfolio_url, wait_until="domcontentloaded")

        assert page.locator("html").get_attribute("data-theme") == "dark"

        browser.close()
