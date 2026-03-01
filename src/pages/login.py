from __future__ import annotations

from playwright.sync_api import Page

from pages.bank_manager.bank_manager_base import BankManagerBasePage
from pages.base import BasePage
from pages.customer.select_customer import SelectCustomerPage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, page_url_path="/login")
        self.button_customer_login = page.locator("button[ng-click=\"customer()\"]")
        self.button_bank_manager_login = page.locator("button[ng-click=\"manager()\"]")

    def open_select_customer_page(self) -> SelectCustomerPage:
        self.button_customer_login.click()
        return SelectCustomerPage(self.page)

    def login_as_bank_manager(self) -> BankManagerBasePage:
        self.button_bank_manager_login.click()
        return BankManagerBasePage(self.page)
