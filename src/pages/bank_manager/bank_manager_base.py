from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page

from pages.base import BasePage

if TYPE_CHECKING:
    from pages.bank_manager.add_account import AddAccountPage
    from pages.bank_manager.add_customer import AddCustomerPage
    from pages.bank_manager.customers import CustomersPage


class BankManagerBasePage(BasePage):
    def __init__(self, page: Page, page_url_path: str = "/manager") -> None:
        super().__init__(page, page_url_path=page_url_path)
        self.button_add_customer = page.locator("button[ng-click=\"addCust()\"]")
        self.button_open_account = page.locator("button[ng-click=\"openAccount()\"]")
        self.button_customers = page.locator("button[ng-click=\"showCust()\"]")

    def open_add_customer_page(self) -> AddCustomerPage:
        from pages.bank_manager.add_customer import AddCustomerPage
        self.button_add_customer.click()
        return AddCustomerPage(self.page)

    def open_add_account_page(self) -> AddAccountPage:
        from pages.bank_manager.add_account import AddAccountPage
        self.button_open_account.click()
        return AddAccountPage(self.page)

    def open_customers_page(self) -> CustomersPage:
        from pages.bank_manager.customers import CustomersPage
        self.button_customers.click()
        return CustomersPage(self.page) \
            .wait_for_page_load()
