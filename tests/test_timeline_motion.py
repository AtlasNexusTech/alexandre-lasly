from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import urlopen

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
        yield f"http://127.0.0.1:{server.server_port}/?timeline-regression=1"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_timeline_dot_stays_attached_to_track_during_reveal(portfolio_url):
    """The timeline content may reveal, but its marker must not leave the track."""
    with urlopen(portfolio_url, timeout=5) as response:
        assert response.status == 200

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(portfolio_url, wait_until="networkidle")
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")

        samples = page.evaluate(
            """
            async () => {
              const timeline = document.querySelector('.timeline');
              const item = timeline.querySelector('.timeline-item');
              const dot = item.querySelector('.timeline-dot');
              const targetY = timeline.getBoundingClientRect().top + scrollY - innerHeight * 0.62;
              scrollTo(0, targetY);

              const deltas = [];
              for (let index = 0; index < 40; index += 1) {
                await new Promise((resolve) => setTimeout(resolve, 20));
                const itemRect = item.getBoundingClientRect();
                const dotRect = dot.getBoundingClientRect();
                const trackStyle = getComputedStyle(item, '::before');
                const trackCenter = itemRect.left
                  + parseFloat(trackStyle.left)
                  + parseFloat(trackStyle.width) / 2;
                const dotCenter = dotRect.left + dotRect.width / 2;
                deltas.push(Math.abs(dotCenter - trackCenter));
              }
              return deltas;
            }
            """
        )
        browser.close()

    assert max(samples) <= 0.1, f"timeline marker detached by {max(samples):.2f}px"
    assert max(samples) - min(samples) <= 0.1, "timeline marker moved relative to track"


def test_mobile_timeline_connects_markers_and_stops_at_last_one(portfolio_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(portfolio_url, wait_until="networkidle")

        geometry = page.locator(".timeline").evaluate(
            """
            (timeline) => {
              const items = [...timeline.querySelectorAll('.timeline-item')];
              return {
                globalTrackDisplay: getComputedStyle(timeline, '::before').display,
                connectors: items.slice(0, -1).map((item, index) => {
                  const itemRect = item.getBoundingClientRect();
                  const style = getComputedStyle(item, '::before');
                  const dotRect = item.querySelector('.timeline-dot').getBoundingClientRect();
                  const nextDotRect = items[index + 1]
                    .querySelector('.timeline-dot').getBoundingClientRect();
                  const trackCenter = itemRect.left
                    + parseFloat(style.left)
                    + parseFloat(style.width) / 2;
                  const connectorTop = itemRect.top + parseFloat(style.top);
                  const connectorBottom = itemRect.bottom - parseFloat(style.bottom);
                  return {
                    content: style.content,
                    centerDelta: Math.abs(
                      dotRect.left + dotRect.width / 2 - trackCenter
                    ),
                    startDelta: Math.abs(
                      dotRect.top + dotRect.height / 2 - connectorTop
                    ),
                    endDelta: Math.abs(
                      nextDotRect.top + nextDotRect.height / 2 - connectorBottom
                    ),
                  };
                }),
                lastConnectorContent: getComputedStyle(items.at(-1), '::before').content,
              };
            }
            """
        )
        browser.close()

    assert geometry["globalTrackDisplay"] == "none"
    assert geometry["lastConnectorContent"] == "none"
    for connector in geometry["connectors"]:
        assert connector["content"] != "none"
        assert connector["centerDelta"] <= 0.1
        assert connector["startDelta"] <= 1
        assert connector["endDelta"] <= 1
