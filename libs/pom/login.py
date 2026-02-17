"""Login page object for XYZ Bank."""

from libs.pom.base import BasePage


class LoginPage(BasePage):
    """XYZ Bank login page. Customer login (dropdown) or Bank Manager login."""

    # Selectors
    CUSTOMER_LOGIN_BTN = "button:has-text('Customer Login')"
    BANK_MANAGER_LOGIN_BTN = "button:has-text('Bank Manager Login')"
    USER_SELECT = "#userSelect"
    LOGIN_BTN = "button[type='submit']"

    def navigate(self) -> None:
        """Open the login page (base URL)."""
        super().navigate("")

    def login_as_customer(self, name: str) -> None:
        """Select customer by visible name and click Login."""
        self.click(self.CUSTOMER_LOGIN_BTN)
        self.page.select_option(self.USER_SELECT, label=name)
        self.click(self.LOGIN_BTN)

    def login_as_bank_manager(self) -> None:
        """Click Bank Manager Login to enter manager section."""
        self.click(self.BANK_MANAGER_LOGIN_BTN)
