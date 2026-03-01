from __future__ import annotations

from typing import Self

from playwright.sync_api import Locator, Page

from pages.components.dropdown import DropdownComponent
from pages.customer.customer_base import CustomerBasePage
from pages.customer.transactions import CustomerTransactionsPage
from testdata.data import CustomerAccountInfo


class CustomerAccountPage(CustomerBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._text_form_label = page.locator("div > label")
        self._button_form_submit = page.locator("button[type=\"submit\"]")
        self._input_form = page.locator("input[ng-model=\"amount\"]")
        self._form_deposit = page.locator("form[ng-submit=\"deposit()\"]")
        # Note: "withdrawl" is intentionally misspelled to match the app's ng-submit attribute
        self._form_withdrawal = page.locator("form[ng-submit=\"withdrawl()\"]")
        self._dropdown_account: Locator = page.locator("#accountSelect")
        self._option_dropdown_account: Locator = self._dropdown_account.locator("option")
        self.text_welcome = page.locator("div.borderM strong:has(.fontBig)")
        self.dropdown_account = DropdownComponent[CustomerAccountPage](
            self._dropdown_account, self._option_dropdown_account, self
        )
        self.text_account_info = page.locator("div[ng-hide=\"noAccount\"]:has(strong)")
        self.button_transactions = page.locator("button[ng-click=\"transactions()\"]")
        self.button_deposit = page.locator("button[ng-click=\"deposit()\"]")
        self.button_withdrawal = page.locator("button[ng-click=\"withdrawl()\"]")
        self.input_deposit_amount = self._form_deposit.locator(self._input_form)
        self.text_deposit_form_label = self._form_deposit.locator(self._text_form_label)
        self.button_deposit_form_submit = self._form_deposit.locator(self._button_form_submit)
        self.input_withdrawal_amount = self._form_withdrawal.locator(self._input_form)
        self.text_withdrawal_form_label = self._form_withdrawal.locator(self._text_form_label)
        self.button_withdrawal_form_submit = self._form_withdrawal.locator(self._button_form_submit)
        self.text_message = page.locator("span[ng-show=\"message\"]")

    def get_welcome_message(self) -> str:
        return self.text_welcome.text_content().strip()

    def open_deposit_form(self) -> Self:
        self.button_deposit.click()
        return self

    def open_withdrawal_form(self) -> Self:
        self.button_withdrawal.click()
        return self

    def open_transactions_page(self) -> CustomerTransactionsPage:
        self.button_transactions.click()
        return CustomerTransactionsPage(self.page) \
            .wait_for_page_load()

    def get_account_info(self) -> CustomerAccountInfo:
        raw_text = self.text_account_info.text_content()
        return CustomerAccountInfo.from_raw_text(raw_text)

    def make_deposit(self, amount: str) -> Self:
        self.input_deposit_amount.fill(amount)
        self.button_deposit_form_submit.click()
        return self

    def make_deposit_if_insufficient_balance(self, amount: int) -> Self:
        account_info = self.get_account_info()
        if account_info.balance < amount:
            deposit_amount = amount - account_info.balance
            self.open_deposit_form()
            self.make_deposit(str(deposit_amount))
        return self

    def make_withdrawal(self, amount: str) -> Self:
        self.input_withdrawal_amount.fill(amount)
        self.button_withdrawal_form_submit.click()
        return self

    def get_message(self) -> str:
        return self.text_message.text_content()
