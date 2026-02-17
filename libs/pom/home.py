"""Customer home page object for XYZ Bank (after customer login)."""

from libs.pom.base import BasePage


class CustomerHomePage(BasePage):
    """Customer account home: welcome message, deposit, withdraw, balance, transactions, logout."""

    # Site uses typo "Withdrawl"
    WELCOME_HEADING = ".fontBig.ng-binding"
    DEPOSIT_BTN = "button:has-text('Deposit')"
    WITHDRAWL_BTN = "button:has-text('Withdrawl')"
    AMOUNT_INPUT = "input[type='number'][placeholder='amount']"
    SUBMIT_AMOUNT_BTN = "button[type='submit']"
    # Balance line is e.g. "Balance : 1000" inside the account box
    BALANCE_ELEMENT = ".borderM.box.padT20 div:has-text('Balance')"
    MESSAGE_ELEMENT = ".error, .ng-binding.ng-scope"
    TRANSACTIONS_BTN = "button:has-text('Transactions')"
    LOGOUT_BTN = "button:has-text('Logout')"
    # After deposit/withdraw, message often in same area
    MESSAGE_SUCCESS = ".error.ng-binding"  # app uses .error for success message text

    def get_welcome_message(self) -> str:
        """Return the welcome message text (e.g. 'Welcome Hermoine Granger')."""
        return self.get_text(self.WELCOME_HEADING).strip()

    def deposit(self, amount: str | int) -> None:
        """Click Deposit, fill amount, submit."""
        amount_str = str(amount)
        self.click(self.DEPOSIT_BTN)
        self.fill(self.AMOUNT_INPUT, amount_str)
        self.click(self.SUBMIT_AMOUNT_BTN)

    def withdraw(self, amount: str | int) -> None:
        """Click Withdrawl (site typo), fill amount, submit."""
        amount_str = str(amount)
        self.click(self.WITHDRAWL_BTN)
        self.fill(self.AMOUNT_INPUT, amount_str)
        self.click(self.SUBMIT_AMOUNT_BTN)

    def get_balance(self) -> str:
        """Return current balance text from the balance display (e.g. 'Balance : 1000')."""
        # Use .last in case multiple accounts; we want the active/updated one
        loc = self.page.locator(self.BALANCE_ELEMENT)
        if loc.count() > 1:
            return loc.last.text_content() or ""
        return self.get_text(self.BALANCE_ELEMENT).strip()

    def get_transaction_count(self) -> int:
        """Return number of rows in transaction list (0 if not on transactions view)."""
        self.click(self.TRANSACTIONS_BTN)
        rows = self.page.locator("table tbody tr").all()
        return len(rows)

    def logout(self) -> None:
        """Click Logout."""
        self.click(self.LOGOUT_BTN)

    def get_message_text(self) -> str:
        """Return visible message after deposit/withdraw (e.g. 'Deposit Successful', 'Transaction successful')."""
        return self.get_text(self.MESSAGE_SUCCESS).strip()
