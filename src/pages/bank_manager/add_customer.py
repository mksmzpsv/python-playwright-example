from __future__ import annotations

from typing import Self

from playwright.sync_api import Page

from pages.bank_manager.bank_manager_base import BankManagerBasePage


class AddCustomerPage(BankManagerBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, page_url_path="/manager/addCust")
        self._form_add_customer = page.locator("form[ng-submit=\"addCustomer()\"]")
        self.input_first_name = self._form_add_customer.locator("input[ng-model=\"fName\"]")
        self.input_last_name = self._form_add_customer.locator("input[ng-model=\"lName\"]")
        self.input_post_code = self._form_add_customer.locator("input[ng-model=\"postCd\"]")
        self.text_first_name_label = self._form_add_customer.locator("div").filter(has=self.input_first_name).locator("label")
        self.text_last_name_label = self._form_add_customer.locator("div").filter(has=self.input_last_name).locator("label")
        self.text_post_code_label = self._form_add_customer.locator("div").filter(has=self.input_post_code).locator("label")
        self.button_add_customer = self._form_add_customer.locator("button[type=\"submit\"]")

    def add_customer(self, first_name: str, last_name: str, post_code: str) -> Self:
        self.input_first_name.fill(first_name)
        self.input_last_name.fill(last_name)
        self.input_post_code.fill(post_code)
        self.button_add_customer.click()
        return self
