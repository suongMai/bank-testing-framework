
from playwright.sync_api import Page


class BasePage:

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def navigate(self, path: str = "") -> None:
        url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url)

    def click(self, selector: str, timeout: float | None = None) -> None:
        """Click element matching selector."""
        self.page.click(selector, timeout=timeout)

    def fill(self, selector: str, value: str, timeout: float | None = None) -> None:
        """Fill input matching selector with value."""
        self.page.fill(selector, value, timeout=timeout)

    def get_text(self, selector: str, timeout: float | None = None) -> str:
        """Return inner text of element matching selector."""
        return self.page.locator(selector).first.text_content(timeout=timeout) or ""

    def get_attribute(self, selector: str, name: str, timeout: float | None = None) -> str | None:
        """Return attribute value of element matching selector."""
        return self.page.locator(selector).first.get_attribute(name, timeout=timeout)

    def is_visible(self, selector: str, timeout: float | None = None) -> bool:
        """Return True if element matching selector is visible."""
        return self.page.locator(selector).first.is_visible(timeout=timeout)

    def wait_for_selector(self, selector: str, state: str = "visible", timeout: float | None = None) -> None:
        """Wait for element matching selector to reach state (visible, hidden, attached, detached)."""
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
