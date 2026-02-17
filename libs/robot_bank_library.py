"""Robot Framework library for XYZ Bank: wraps POM and manages browser lifecycle."""

import json
import os
import re
from typing import Any, List

from playwright.sync_api import sync_playwright, Page

from libs.browser_factory import create_browser
from libs.pom.login import LoginPage
from libs.pom.home import CustomerHomePage
from libs.pom.manager import ManagerPage


# Default base URL for XYZ Bank demo
DEFAULT_BASE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"


class BankingLibrary:
    """
    Robot Framework library for XYZ Bank automation.
    """

    ROBOT_LIBRARY_SCOPE = "SUITE"  # one browser per test suite
    ROBOT_LIBRARY_VERSION = "1.0"

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        browser: str = "chromium",
        headless: bool = True,
    ):
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.browser_name = self._normalize_browser(browser)
        # Robot passes "True"/"False" as strings
        self.headless = str(headless).lower() in ("true", "1", "yes") if headless is not None else True
        self._playwright_cm = None  # sync_playwright() context manager
        self._browser = None
        self._context = None
        self._page: Optional[Page] = None
        self._login_page: Optional[LoginPage] = None
        self._home_page: Optional[CustomerHomePage] = None
        self._manager_page: Optional[ManagerPage] = None

    @staticmethod
    def _normalize_browser(name: str) -> str:
        n = (name or "chromium").lower().strip()
        if n == "chrome":
            return "chromium"
        if n == "edge":
            return "msedge"
        return n

    def _ensure_browser(self) -> Page:
        if self._page is not None:
            return self._page
        self._playwright_cm = sync_playwright()
        playwright = self._playwright_cm.__enter__()
        self._browser = create_browser(
            playwright,
            self.browser_name,
            headless=self.headless,
        )
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        base = self.base_url
        self._page.goto(base, timeout=60000, wait_until="domcontentloaded")
        self._login_page = LoginPage(self._page, base)
        self._home_page = CustomerHomePage(self._page, base)
        self._manager_page = ManagerPage(self._page, base)
        return self._page

    def open_bank_login_page(self) -> None:
        self._ensure_browser()

    def navigate_to_login_page(self) -> None:
        self._ensure_browser()
        self._page.goto(self.base_url, timeout=60000, wait_until="domcontentloaded")

    def login_as_customer(self, customer_name: str) -> None:
        self._ensure_browser()
        self._login_page.login_as_customer(customer_name)

    def login_as_bank_manager(self) -> None:
        self._ensure_browser()
        self._login_page.login_as_bank_manager()

    def get_welcome_message(self) -> str:
        self._ensure_browser()
        return self._home_page.get_welcome_message()

    def deposit_amount(self, amount: str | int) -> None:
        self._ensure_browser()
        self._home_page.deposit(amount)

    def withdraw_amount(self, amount: str | int) -> None:
        self._ensure_browser()
        self._home_page.withdraw(amount)

    def get_balance_text(self) -> str:
        
        self._ensure_browser()
        return self._home_page.get_balance()

    def get_balance_number(self) -> int:
        text = self.get_balance_text()
        match = re.search(r"(\d+)", text.replace(",", ""))
        if not match:
            raise ValueError(f"Could not parse balance from: {text!r}")
        return int(match.group(1))

    def get_message_text(self) -> str:
        self._ensure_browser()
        return self._home_page.get_message_text()

    def wait_for_ui(self, milliseconds: int = 1500) -> None:
        self._ensure_browser()
        self._page.wait_for_timeout(milliseconds)

    def verify_deposit_successful(self) -> None:
        msg = self.get_message_text()
        if "Deposit Successful" not in msg and "deposit successful" not in msg.lower():
            raise AssertionError(f"Expected deposit success message, got: {msg!r}")

    def verify_withdraw_success_message(self) -> None:
        msg = self.get_message_text()
        if not msg:
            return
        ok = (
            "Transaction successful" in msg
            or "transaction successful" in msg.lower()
            or "Withdraw" in msg
        )
        if not ok:
            raise AssertionError(f"Unexpected message after withdraw: {msg!r}")

    def add_customer(self, first_name: str, last_name: str, post_code: str) -> None:
        self._ensure_browser()
        self._manager_page.add_customer(first_name, last_name, post_code)

    def add_customer_and_accept_alert(self, first_name: str, last_name: str, post_code: str) -> str:
        
        self._ensure_browser()
        alerts = []

        def on_dialog(dialog):
            alerts.append(dialog.message)
            dialog.accept()

        self._page.once("dialog", on_dialog)
        self._manager_page.add_customer(first_name, last_name, post_code)
        if not alerts:
            raise AssertionError("Expected one alert after Add Customer")
        return alerts[0]

    def verify_customer_added_alert(self, alert_message: str) -> None:
        if "Customer added" not in alert_message and "success" not in alert_message.lower():
            raise AssertionError(f"Expected success in alert, got: {alert_message!r}")

    
    def _load_test_data(self, file_path: str) -> dict:
        path = os.path.normpath(os.path.abspath(file_path))
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Test data file not found: {path}")
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def get_deposit_test_data(self, file_path: str) -> List[Any]:
        data = self._load_test_data(file_path)
        rows = data.get("customer_deposits", [])
        result = []
        for r in rows:
            result.append(r["customer_name"])
            result.append(int(r["amount"]))
        return result

    def get_withdrawal_test_data(self, file_path: str) -> List[Any]:
        data = self._load_test_data(file_path)
        rows = data.get("customer_withdrawals", [])
        result = []
        for r in rows:
            result.append(r["customer_name"])
            result.append(int(r["deposit_amount"]))
            result.append(int(r["withdraw_amount"]))
        return result

    def get_add_customer_test_data(self, file_path: str) -> List[Any]:
        data = self._load_test_data(file_path)
        rows = data.get("manager_add_customers", [])
        result = []
        for r in rows:
            result.append(r["first_name"])
            result.append(r["last_name"])
            result.append(r["post_code"])
        return result

    def run_deposit_test_with_data(self, customer_name: str, amount: int) -> None:
        """Execute one deposit flow: navigate to login, login as customer, deposit amount, verify message and balance."""
        self.navigate_to_login_page()
        self.login_as_customer(customer_name)
        welcome = self.get_welcome_message()
        if customer_name and customer_name.split()[0] not in welcome:
            raise AssertionError(f"Welcome should contain customer name, got: {welcome!r}")
        balance_before = self.get_balance_number()
        self.deposit_amount(amount)
        self.verify_deposit_successful()
        self.wait_for_ui(1500)
        balance_after = self.get_balance_number()
        if balance_after < balance_before:
            raise AssertionError(
                f"Balance should not decrease after deposit: was {balance_before}, got {balance_after}"
            )

    def run_withdrawal_test_with_data(
        self, customer_name: str, deposit_amount: int, withdraw_amount: int
    ) -> None:
        """Execute one withdrawal flow: login, deposit, withdraw, verify message and balance."""
        self.navigate_to_login_page()
        self.login_as_customer(customer_name)
        self.deposit_amount(deposit_amount)
        self.wait_for_ui(1500)
        self.withdraw_amount(withdraw_amount)
        self.wait_for_ui(1500)
        self.verify_withdraw_success_message()
        balance = self.get_balance_number()
        if balance < 0:
            raise AssertionError(f"Balance should be non-negative, got {balance}")

    def run_add_customer_test_with_data(
        self, first_name: str, last_name: str, post_code: str
    ) -> None:
        """Execute one add-customer flow: login as manager, add customer, accept alert, verify success."""
        self.navigate_to_login_page()
        self.login_as_bank_manager()
        alert_msg = self.add_customer_and_accept_alert(first_name, last_name, post_code)
        self.verify_customer_added_alert(alert_msg)

    def close_browser(self) -> None:
        """Close browser and Playwright (Suite Teardown)."""
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright_cm is not None:
            try:
                self._playwright_cm.__exit__(None, None, None)
            except Exception:
                pass
            self._playwright_cm = None
        self._page = None
        self._login_page = None
        self._home_page = None
        self._manager_page = None
