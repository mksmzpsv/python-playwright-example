from __future__ import annotations

import os
from typing import TYPE_CHECKING, Self

from playwright.sync_api import Dialog, Locator, Page

from pages.abstract_page import AbstractPage

if TYPE_CHECKING:
    from pages.login import LoginPage


class BasePage(AbstractPage):
    def __init__(self, page: Page, page_url_path: str = "") -> None:
        self._base_url: str = (
            os.getenv("BASE_URL")
            or "https://www.globalsqa.com/angularJs-protractor/BankingProject/#"
        )
        self._page_url_path = page_url_path
        self.page: Page = page
        self.header: Locator = page.locator(".box.mainhdr")
        self.button_home: Locator = self.header.locator(".button.home")
        self.text_header: Locator = self.header.locator(".mainHeading")

    def open(self) -> Self:
        self.page.goto(f"{self._base_url}{self._page_url_path}")
        return self

    def wait_for_page_load(self) -> Self:
        self.page.wait_for_url(f"{self._base_url}{self._page_url_path}")
        self.page.wait_for_load_state("load")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def open_login_page(self) -> LoginPage:
        self.button_home.click()
        return LoginPage(self.page)

    def dialog_handler(self, messages: list[str]):
        def handler(dialog: Dialog) -> None:
            messages.append(dialog.message)
            dialog.accept()
        return handler
