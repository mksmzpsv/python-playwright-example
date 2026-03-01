from __future__ import annotations

from collections.abc import Callable
from typing import Any

from playwright.sync_api import Locator

from pages.abstract_page import AbstractPage


class TableComponent[T: AbstractPage]:
    def __init__(
        self,
        table_locator: Locator,
        header_locator: Locator,
        row_locator: Locator,
        cell_locator: Locator,
        page: T | None = None,
    ):
        self._page = page
        self.table = table_locator
        self.headers = self.table.locator(header_locator)
        self.rows = self.table.locator(row_locator)
        self.cell_locator = cell_locator

    def get_column_index_by_header_name(self, header_name: str) -> int:
        header_count = self.headers.count()
        for i in range(header_count):
            text = self.headers.nth(i).inner_text().strip()
            if text == header_name:
                return i
        raise ValueError(f"Header '{header_name}' not found")

    def get_cell_value(self, row_index: int, header_name: str) -> str:
        column_index = self.get_column_index_by_header_name(header_name)
        row = self.rows.nth(row_index)
        cell = row.locator(self.cell_locator).nth(column_index)
        return cell.inner_text().strip()

    def find_row_index(self, header_name: str, value: str) -> int:
        column_index = self.get_column_index_by_header_name(header_name)
        row_count = self.rows.count()
        for row_idx in range(row_count):
            row = self.rows.nth(row_idx)
            cell = row.locator(self.cell_locator).nth(column_index)
            cell_value = cell.inner_text().strip()
            if cell_value == value:
                return row_idx
        return -1

    def get_columns_headers(self) -> list[str]:
        header_count = self.headers.count()
        actual_headers = []
        for i in range(header_count):
            text = self.headers.nth(i).inner_text().strip()
            actual_headers.append(text)
        return actual_headers

    def is_column_sorted(
        self,
        column_header: str,
        ascending: bool,
        key: Callable[[str], Any] | None = None,
    ) -> bool:
        rows_count = self.rows.count()
        values = []
        for i in range(rows_count):
            cell_value = self.get_cell_value(i, column_header)
            values.append(cell_value)
        sorted_values = sorted(values, key=key, reverse=not ascending)
        return values == sorted_values

    def get_row_as_dict(self, row_index: int) -> dict[str, str]:
        row_dict = {}
        headers = self.get_columns_headers()
        row = self.rows.nth(row_index)
        cells = row.locator(self.cell_locator)
        for i, header in enumerate(headers):
            row_dict[header] = cells.nth(i).inner_text().strip()
        return row_dict

    def sort_column(
        self,
        column_header: str,
        ascending: bool,
        key: Callable[[str], Any] | None = None,
    ) -> T | None:
        header_link = self.headers.filter(has_text=column_header).locator("a")
        is_sorted_ascending = self.is_column_sorted(column_header, ascending=True, key=key)
        if ascending and not is_sorted_ascending:
            header_link.click()
        elif not ascending and is_sorted_ascending:
            header_link.click()
        return self._page
