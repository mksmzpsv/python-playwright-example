from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self

from playwright.sync_api import Page


class AbstractPage(ABC):
    page: Page
    _base_url: str
    _page_url_path: str

    @abstractmethod
    def open(self) -> Self: ...

    @abstractmethod
    def wait_for_page_load(self) -> Self: ...
