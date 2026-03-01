from __future__ import annotations

from playwright.sync_api import Locator

from pages.abstract_page import AbstractPage


class DropdownComponent[T: AbstractPage]:
    def __init__(
        self,
        dropdown_locator: Locator,
        options_locator: Locator,
        page: T | None = None,
    ):
        self.dropdown = dropdown_locator
        self.options = options_locator
        self._page = page

    def select_option_by_inner_text(self, text: str) -> T | None:
        self.dropdown.select_option(label=text)
        return self._page

    def select_option_by_index(self, index: int) -> T | None:
        self.dropdown.select_option(index=index)
        return self._page

    def select_option_by_value(self, value: str) -> T | None:
        self.dropdown.select_option(value=value)
        return self._page

    def get_selected_option_text(self) -> str:
        raw_value = self.dropdown.input_value()
        if ":" in raw_value:
            return raw_value.split(":", 1)[1].strip()
        return raw_value.strip()

    def get_options_count(self) -> int:
        return self.options.count()
