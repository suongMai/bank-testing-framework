"""Manager page object for XYZ Bank (Bank Manager section)."""

from libs.pom.base import BasePage


class ManagerPage(BasePage):
    """Bank Manager: Add Customer, Open Account, Customers list."""

    ADD_CUSTOMER_BTN = "button:has-text('Add Customer')"
    OPEN_ACCOUNT_BTN = "button:has-text('Open Account')"
    CUSTOMERS_BTN = "button:has-text('Customers')"
    # Add Customer form
    FIRST_NAME_INPUT = "input[placeholder='First Name']"
    LAST_NAME_INPUT = "input[placeholder='Last Name']"
    POST_CODE_INPUT = "input[placeholder='Post Code']"
    ADD_CUSTOMER_SUBMIT_BTN = "button[type='submit']"
    # Open Account form
    CUSTOMER_SELECT = "#userSelect"
    CURRENCY_SELECT = "#currency"
    PROCESS_BTN = "button[type='submit']"

    def add_customer(self, f_name: str, l_name: str, post_code: str) -> None:
        """Fill Add Customer form and submit. Alert with success message may appear."""
        self.click(self.ADD_CUSTOMER_BTN)
        self.fill(self.FIRST_NAME_INPUT, f_name)
        self.fill(self.LAST_NAME_INPUT, l_name)
        self.fill(self.POST_CODE_INPUT, post_code)
        self.click(self.ADD_CUSTOMER_SUBMIT_BTN)

    def open_account(self, customer_name: str, currency: str) -> None:
        """Open account for customer with given currency."""
        self.click(self.OPEN_ACCOUNT_BTN)
        self.page.select_option(self.CUSTOMER_SELECT, label=customer_name)
        self.page.select_option(self.CURRENCY_SELECT, label=currency)
        self.click(self.PROCESS_BTN)

    def goto_customers_list(self) -> None:
        """Navigate to the Customers list view."""
        self.click(self.CUSTOMERS_BTN)
