from collections.abc import Callable

import pytest
from playwright.sync_api import Page

from pages.bank_manager.bank_manager_base import BankManagerBasePage
from pages.bank_manager.customers import CustomersPage
from pages.customer.account import CustomerAccountPage
from pages.customer.select_customer import SelectCustomerPage
from pages.login import LoginPage


@pytest.fixture
def open_select_customer_page(page: Page) -> SelectCustomerPage:
    login_page = LoginPage(page)
    select_customer_page = login_page \
        .open() \
        .open_select_customer_page()
    return select_customer_page


@pytest.fixture
def login_as_specific_customer(
    open_select_customer_page: SelectCustomerPage,
) -> Callable[[str], CustomerAccountPage]:
    def _login_as_customer(customer_name: str) -> CustomerAccountPage:
        customer_selection_page: SelectCustomerPage = open_select_customer_page
        customer_account_page = customer_selection_page.dropdown_customer \
            .select_option_by_inner_text(customer_name) \
            .login_as_customer()
        assert customer_account_page \
            .get_welcome_message() == f"Welcome {customer_name} !!", \
            "Welcome message is incorrect"
        return customer_account_page
    return _login_as_customer


@pytest.fixture
def login_as_bank_manager(page: Page) -> BankManagerBasePage:
    login_page = LoginPage(page)
    manager_page = login_page \
        .open() \
        .login_as_bank_manager()
    return manager_page


@pytest.fixture
def add_customer(
    login_as_bank_manager: BankManagerBasePage,
) -> CustomersPage:
    def _add_customer(first_name: str, last_name: str, post_code: str) -> CustomersPage:
        bank_manager_base_page: BankManagerBasePage = login_as_bank_manager
        bank_manager_base_page \
            .open_add_customer_page() \
            .add_customer(first_name, last_name, post_code)
        return bank_manager_base_page.open_customers_page()
    return _add_customer
