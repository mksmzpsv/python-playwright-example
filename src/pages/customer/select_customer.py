from __future__ import annotations

from playwright.sync_api import Locator, Page

from pages.base import BasePage
from pages.components.dropdown import DropdownComponent
from pages.customer.account import CustomerAccountPage


class SelectCustomerPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, page_url_path="/customer")
        self._form_select_customer: Locator = page.locator("form[ng-submit=\"showAccount()\"]")
        self._dropdown_customer: Locator = self._form_select_customer.locator("#userSelect")
        self._option_dropdown_customer: Locator = self._dropdown_customer.locator("option[ng-repeat=\"cust in Customers\"]")
        self.text_select_customer_label: Locator = self._form_select_customer.locator("div > label")
        self.dropdown_customer = DropdownComponent[SelectCustomerPage](self._dropdown_customer, self._option_dropdown_customer, self)
        self.button_login: Locator = self._form_select_customer.locator("button[type=\"submit\"]")

    def login_as_customer(self) -> CustomerAccountPage:
        self.button_login.click()
        return CustomerAccountPage(self.page)
