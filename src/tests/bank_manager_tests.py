from playwright.sync_api import Page

from pages.bank_manager.bank_manager_base import BankManagerBasePage
from pages.bank_manager.customers import CustomersPage
from testdata.data import CustomerInfo

def test_bank_manager_adds_customer(
    login_as_bank_manager: BankManagerBasePage,
    page: Page,
):
    messages: list[str] = []
    first_name = "Test"
    last_name = "Customer"
    post_code = "12345"

    bank_manager_base_page: BankManagerBasePage = login_as_bank_manager
    page.on("dialog", bank_manager_base_page.dialog_handler(messages))
    bank_manager_base_page \
        .open_add_customer_page() \
        .add_customer(first_name, last_name, post_code)
    assert "Customer added successfully with customer id" in messages[0], \
        f"Unexpected dialog message: '{messages[0]}'"
    customer_info: CustomerInfo = bank_manager_base_page \
        .open_customers_page() \
        .search_customer(first_name) \
        .get_customer(row_index=0)
    assert customer_info.first_name == first_name, \
        "First name of the added customer is incorrect"
    assert customer_info.last_name == last_name, \
        "Last name of the added customer is incorrect"
    assert customer_info.post_code == post_code, \
        "Post code of the added customer is incorrect"
    assert customer_info.account_number == "", \
        "Newly added customer should not have any accounts"


def test_bank_manager_open_account_for_customer(
    login_as_bank_manager: BankManagerBasePage,
    page: Page,
):
    messages: list[str] = []
    customer_first_name = "Ron"
    customer_last_name = "Weasly"
    customer_full_name = f"{customer_first_name} {customer_last_name}"
    account_currency = "Dollar"

    bank_manager_base_page: BankManagerBasePage = login_as_bank_manager
    page.on("dialog", bank_manager_base_page.dialog_handler(messages))
    bank_manager_base_page \
        .open_add_account_page() \
        .open_account_for_customer(customer_full_name, account_currency)
    assert "Account created successfully with account Number" in messages[0], \
        f"Unexpected dialog message: '{messages[0]}'"
    account_number = messages[0].split(":")[1].strip()
    customer_info: CustomerInfo = bank_manager_base_page \
        .open_customers_page() \
        .search_customer(account_number) \
        .get_customer(row_index=0)
    assert customer_info.first_name == customer_first_name, \
        "First name of the customer is incorrect, searching customer by account number should return correct result"
    assert customer_info.last_name == customer_last_name, \
        "Last name of the customer is incorrect, searching customer by account number should return correct result"
    assert account_number in customer_info.account_number, (
        "Account number in the dialog message does not match "
        "the account number in the customer table"
    )

def test_bank_manager_deletes_customer(
    add_customer: CustomersPage,
):
    customer_first_name = "TestCustomerToDelete"
    customer_last_name = "Customer"
    post_code = "12345"

    customers_page: CustomersPage = add_customer(customer_first_name, customer_last_name, post_code)
    customers_page \
        .search_customer(customer_first_name) \
        .delete_customer_with(column_name=CustomerInfo.FIRST_NAME_KEY, value=customer_first_name)
    assert customers_page.table_customers.rows.count() == 0, \
        "Customer was not deleted successfully, expected 0 search results after deletion"

