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


def test_dark_theme_is_default_on_desktop_even_when_system_prefers_light(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800}, color_scheme="light")
        page = context.new_page()
        page.goto(portfolio_url, wait_until="networkidle")

        assert page.locator("html").get_attribute("data-theme") == "dark"
        assert page.locator("[data-theme-toggle]").get_attribute("aria-label") == "Utiliser le thème clair"

        browser.close()


def test_light_theme_is_default_on_mobile_even_when_system_prefers_dark(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844}, color_scheme="dark")
        page = context.new_page()
        page.goto(portfolio_url, wait_until="networkidle")

        assert page.locator("html").get_attribute("data-theme") == "light"
        assert page.locator("[data-theme-toggle]").get_attribute("aria-label") == "Utiliser le thème sombre"

        browser.close()


@pytest.mark.parametrize(
    ("viewport", "saved_theme"),
    [
        ({"width": 390, "height": 844}, "dark"),
        ({"width": 1280, "height": 800}, "light"),
    ],
)
def test_saved_theme_overrides_responsive_default(portfolio_url, viewport, saved_theme):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport=viewport)
        context.add_init_script(
            f"localStorage.setItem('alexandre-lasly-theme', {saved_theme!r})"
        )
        page = context.new_page()
        page.goto(portfolio_url, wait_until="networkidle")

        assert page.locator("html").get_attribute("data-theme") == saved_theme

        browser.close()


def test_blocked_local_storage_does_not_stop_theme_or_navigation(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844})
        context.add_init_script(
            """
            for (const method of ['getItem', 'setItem']) {
              Object.defineProperty(Storage.prototype, method, {
                configurable: true,
                value() { throw new DOMException('Storage blocked', 'SecurityError'); },
              });
            }
            """
        )
        page = context.new_page()
        page_errors = []
        page.on("pageerror", lambda error: page_errors.append(str(error)))
        page.goto(portfolio_url, wait_until="networkidle")

        assert page_errors == []
        assert page.locator("html").get_attribute("data-theme") == "light"

        page.locator("[data-theme-toggle]").click()
        assert page.locator("html").get_attribute("data-theme") == "dark"

        page.locator("[data-menu-toggle]").click()
        assert page.locator("[data-menu-toggle]").get_attribute("aria-expanded") == "true"

        browser.close()


def test_dark_theme_is_applied_before_external_javascript_on_desktop(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800}, color_scheme="light")
        page = context.new_page()
        page.route("**/script.js*", lambda route: route.abort())
        page.goto(portfolio_url, wait_until="domcontentloaded")

        assert page.locator("html").get_attribute("data-theme") == "dark"

        browser.close()


def test_light_theme_is_applied_before_external_javascript_on_mobile(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844}, color_scheme="dark")
        page = context.new_page()
        page.route("**/script.js*", lambda route: route.abort())
        page.goto(portfolio_url, wait_until="domcontentloaded")

        assert page.locator("html").get_attribute("data-theme") == "light"

        browser.close()


def test_primary_contact_button_meets_wcag_contrast_in_dark_theme(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(portfolio_url, wait_until="networkidle")

        contrast_ratio = page.locator("[data-contact-reveal]").evaluate(
            """
            (element) => {
              const parse = (color) => color.match(/[\\d.]+/g).slice(0, 3).map(Number);
              const luminance = (rgb) => {
                const channels = rgb.map((value) => {
                  const channel = value / 255;
                  return channel <= 0.04045
                    ? channel / 12.92
                    : ((channel + 0.055) / 1.055) ** 2.4;
                });
                return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
              };
              const style = getComputedStyle(element);
              const foreground = luminance(parse(style.color));
              const background = luminance(parse(style.backgroundColor));
              return (Math.max(foreground, background) + 0.05)
                / (Math.min(foreground, background) + 0.05);
            }
            """
        )

        assert contrast_ratio >= 4.5

        browser.close()


def test_dark_section_kicker_meets_wcag_contrast_in_mobile_light_theme(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        page.goto(portfolio_url, wait_until="networkidle")

        contrast_ratio = page.locator(".section-dark .kicker").evaluate(
            """
            (element) => {
              const parse = (color) => color.match(/[\\d.]+/g).slice(0, 3).map(Number);
              const luminance = (rgb) => {
                const channels = rgb.map((value) => {
                  const channel = value / 255;
                  return channel <= 0.04045
                    ? channel / 12.92
                    : ((channel + 0.055) / 1.055) ** 2.4;
                });
                return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
              };
              const style = getComputedStyle(element);
              const foreground = luminance(parse(style.color));
              const background = luminance(parse(style.backgroundColor));
              const sectionBackground = luminance(
                parse(getComputedStyle(element.closest('.section-dark')).backgroundColor)
              );
              const effectiveBackground = style.backgroundColor === 'rgba(0, 0, 0, 0)'
                ? sectionBackground
                : background;
              return (Math.max(foreground, effectiveBackground) + 0.05)
                / (Math.min(foreground, effectiveBackground) + 0.05);
            }
            """
        )

        assert contrast_ratio >= 4.5

        browser.close()
