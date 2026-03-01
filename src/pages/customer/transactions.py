from __future__ import annotations

from typing import TYPE_CHECKING, Self

from playwright.sync_api import Page

from pages.components.table import TableComponent
from pages.customer.customer_base import CustomerBasePage
from testdata.data import TransactionInfo
from utils.date_utils import parse_date_time

if TYPE_CHECKING:
    from pages.customer.account import CustomerAccountPage


class CustomerTransactionsPage(CustomerBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page, page_url_path="/listTx")
        self.table_transactions = TableComponent[CustomerTransactionsPage](
            table_locator=page.locator("table"),
            header_locator=page.locator("thead tr td"),
            row_locator=page.locator("tbody tr"),
            cell_locator=page.locator("td"),
            page=self
        )
        self.button_back_to_account = page.locator("button[ng-click=\"back()\"]")
        self.input_start_date = page.locator("div[ng-show=\"showDate\"] input#start")
        self.input_end_date = page.locator("div[ng-show=\"showDate\"] input#end")
        self.button_reset = page.locator("button[ng-click=\"reset()\"]")
        self.link_transaction_table_sort_date = self.table_transactions.table.locator("thead a[ng-click*=\"date\"]")
        self.button_previous_page = page.locator("[ng-click=\"scrollLeft()\"]")
        self.button_next_page = page.locator("[ng-click=\"scrollRight()\"]")
        self.button_top = page.locator("[ng-click=\"scrollTop()\"]")

    def back_to_customer_account(self) -> CustomerAccountPage:
        self.button_back_to_account.click()
        return CustomerAccountPage(self.page)

    def get_transaction(self, row_index: int) -> TransactionInfo:
        row_dict = self.table_transactions.get_row_as_dict(row_index)
        return TransactionInfo.from_dict(row_dict)

    def reset_transactions(self) -> Self:
        self.button_reset.click()
        return self

    # TODO: Added this method to handle the flaky behavior of the transactions table not loading transactions after performing a deposit/withdrawal and navigating to the transactions page.
    # Potential issue with the demo app itself. Should be investigated further, and this workaround should be removed if the issue is fixed in the app.
    def reload_transactions_if_table_empty(self, attempts: int = 3) -> Self:
        remaining_attempts = attempts
        while self.table_transactions.rows.count() == 0 and remaining_attempts > 0:
            self.page.reload()
            self.wait_for_page_load()
            remaining_attempts -= 1
        return self

    def is_date_time_column_sorted(self, ascending: bool) -> bool:
        return self.table_transactions.is_column_sorted(
            TransactionInfo.DATE_TIME_KEY,
            ascending=ascending,
            key=parse_date_time,
        )

    def sort_by_date_time(self, ascending: bool) -> Self:
        self.table_transactions.sort_column(
            TransactionInfo.DATE_TIME_KEY,
            ascending=ascending,
            key=parse_date_time,
        )
        return self
