from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from pages.base import BasePage

if TYPE_CHECKING:
    from pages.customer.select_customer import SelectCustomerPage


class CustomerBasePage(BasePage):
    def __init__(self, page: Page, page_url_path: str = "/account") -> None:
        super().__init__(page, page_url_path=page_url_path)
        self.button_logout: Locator = self.header.locator(".button.logout")

    def logout(self) -> SelectCustomerPage:
        from pages.customer.select_customer import SelectCustomerPage
        self.button_logout.click()
        return SelectCustomerPage(self.page)

