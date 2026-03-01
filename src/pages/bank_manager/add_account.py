from __future__ import annotations

from typing import Self

from playwright.sync_api import Page

from pages.bank_manager.bank_manager_base import BankManagerBasePage
from pages.components.dropdown import DropdownComponent


class AddAccountPage(BankManagerBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, page_url_path="/manager/openAccount")
        self._dropdown_customer = page.locator("#userSelect")
        self._option_dropdown_customer = self._dropdown_customer.locator("option[ng-repeat=\"cust in Customers\"]")
        self._dropdown_currency = page.locator("#currency")
        self._option_dropdown_currency = self._dropdown_currency.locator("option")
        self._form_open_account = page.locator("form[ng-submit=\"process()\"]")
        self.dropdown_customer: DropdownComponent[AddAccountPage] = DropdownComponent(self._dropdown_customer, self._option_dropdown_customer, self)
        self.dropdown_currency: DropdownComponent[AddAccountPage] = DropdownComponent(self._dropdown_currency, self._option_dropdown_currency, self)
        self.text_select_customer_label = self._form_open_account.locator("div").filter(has=self._dropdown_customer).locator("label")
        self.text_select_currency_label = self._form_open_account.locator("div").filter(has=self._dropdown_currency).locator("label")
        self.button_process = self._form_open_account.locator("button[type=\"submit\"]")

    def open_account_for_customer(self, customer_name: str, currency: str) -> Self:
        self.dropdown_customer.select_option_by_inner_text(customer_name)
        self.dropdown_currency.select_option_by_inner_text(currency)
        self.button_process.click()
        return self
