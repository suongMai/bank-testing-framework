"""Factory for creating Playwright browser instances by name."""

from playwright.sync_api import Playwright, Browser

# Supported browser names (after resolving aliases)
CHROMIUM = "chromium"
FIREFOX = "firefox"
MSEDGE = "msedge"


def create_browser(playwright: Playwright, browser_name: str, **launch_options) -> Browser:
    """
    Create and return a launched browser for the given name.

    Args:
        playwright: Playwright instance from sync_playwright().
        browser_name: One of 'chromium', 'firefox', 'msedge'.
        **launch_options: Passed to launch() (e.g. headless=True).

    Returns:
        Launched Browser instance.
    """
    name = (browser_name or "").lower().strip()
    if name == FIREFOX:
        return playwright.firefox.launch(**launch_options)
    if name == MSEDGE:
        return playwright.chromium.launch(channel="msedge", **launch_options)
    # chromium (default) and any unknown fall back to Chromium
    return playwright.chromium.launch(**launch_options)
