from __future__ import annotations

from typing import Self

from playwright.sync_api import Page

from pages.bank_manager.bank_manager_base import BankManagerBasePage
from pages.components.table import TableComponent
from testdata.data import CustomerInfo


class CustomersPage(BankManagerBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, page_url_path="/manager/list")
        self.table_customers = TableComponent[CustomersPage](
            table_locator=page.locator("table.table-bordered"),
            header_locator=page.locator("thead tr td"),
            row_locator=page.locator("tbody tr"),
            cell_locator=page.locator("td"),
            page=self
        )
        self.input_search_customer = page.locator("input[ng-model=\"searchCustomer\"]")
        self.button_delete_customer = page.locator("button[ng-click=\"deleteCust(cust)\"]")

    def search_customer(self, search_query: str) -> Self:
        self.input_search_customer.fill(search_query)
        return self

    def get_customer(self, row_index: int) -> CustomerInfo:
        row_dict = self.table_customers.get_row_as_dict(row_index)
        return CustomerInfo.from_dict(row_dict)

    def delete_customer_with(self, column_name: str, value: str) -> Self:
        row_index = self.table_customers.find_row_index(column_name, value)
        if row_index == -1:
            raise ValueError(f"Customer with {column_name} '{value}' not found")
        self.table_customers.rows.nth(row_index).locator(self.button_delete_customer).click()
        return self
