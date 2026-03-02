from playwright.sync_api import Page

from fixtures.fixtures import login_as_specific_customer
from pages.customer.account import CustomerAccountPage
from pages.customer.transactions import CustomerTransactionsPage
from testdata.data import TransactionInfo


def test_customer_makes_deposit(
    login_as_specific_customer: CustomerAccountPage,
    page: Page,
):
    customer_name = "Albus Dumbledore"
    deposit_amount: int = 100

    customer_account_page: CustomerAccountPage = login_as_specific_customer(customer_name)
    current_account_info = customer_account_page \
        .wait_for_page_load() \
        .get_account_info()
    deposit_success_message = customer_account_page \
        .open_deposit_form() \
        .make_deposit(str(deposit_amount)) \
        .wait_for_page_load() \
        .get_message()
    updated_account_info = customer_account_page \
        .get_account_info()
    assert deposit_success_message == "Deposit Successful", \
        "Message after making deposit is incorrect"
    assert updated_account_info.balance == current_account_info.balance + deposit_amount, \
        "Account balance after deposit is incorrect"
    assert customer_account_page.dropdown_account \
        .get_selected_option_text() == str(updated_account_info.number), \
        "Selected account after making deposit is incorrect"
    transactions_page: CustomerTransactionsPage = customer_account_page \
        .open_transactions_page() \
        .wait_for_page_load() \
        .reload_transactions_if_table_empty() \
        .sort_by_date_time(ascending=False)
    assert transactions_page.is_date_time_column_sorted(ascending=False), \
        "Transactions are not sorted by Date-Time in descending order"
    latest_transaction: TransactionInfo = transactions_page \
        .get_transaction(row_index=0)
    assert latest_transaction.amount == deposit_amount, \
        "Latest transaction amount is incorrect"
    assert latest_transaction.transaction_type == "Credit", \
        "Latest transaction type is incorrect"


def test_customer_makes_withdrawal(
    login_as_specific_customer: CustomerAccountPage,
    page: Page,
):
    customer_name = "Neville Longbottom"
    withdrawal_amount: int = 10

    customer_account_page: CustomerAccountPage = login_as_specific_customer(customer_name)
    current_account_info = customer_account_page \
        .wait_for_page_load() \
        .make_deposit_if_insufficient_balance(withdrawal_amount) \
        .get_account_info()
    withdrawal_success_message = customer_account_page \
        .open_withdrawal_form() \
        .make_withdrawal(str(withdrawal_amount)) \
        .wait_for_page_load() \
        .get_message()
    updated_account_info = customer_account_page \
        .get_account_info()
    assert withdrawal_success_message == "Transaction successful", \
        "Message after making withdrawal is incorrect"
    assert updated_account_info.balance == current_account_info.balance - withdrawal_amount, \
        "Account balance after withdrawal is incorrect"
    assert customer_account_page.dropdown_account \
        .get_selected_option_text() == str(updated_account_info.number), \
        "Selected account after making withdrawal is incorrect"
    transactions_page: CustomerTransactionsPage = customer_account_page \
        .open_transactions_page() \
        .wait_for_page_load() \
        .reload_transactions_if_table_empty() \
        .sort_by_date_time(ascending=False)
    assert transactions_page.is_date_time_column_sorted(ascending=False), \
        "Transactions are not sorted by Date-Time in descending order"
    latest_transaction: TransactionInfo = transactions_page \
        .get_transaction(row_index=0)
    assert latest_transaction.amount == withdrawal_amount, \
        "Latest transaction amount is incorrect"
    assert latest_transaction.transaction_type == "Debit", \
        "Latest transaction type is incorrect"


def test_customer_makes_withdrawal_with_insufficient_balance(
    login_as_specific_customer: CustomerAccountPage,
    page: Page,
):
    customer_name = "Hermoine Granger"

    customer_account_page: CustomerAccountPage = login_as_specific_customer(customer_name)
    current_account_info = customer_account_page \
        .wait_for_page_load() \
        .get_account_info()
    withdrawal_amount = current_account_info.balance + 1
    withdrawal_message = customer_account_page \
        .open_withdrawal_form() \
        .make_withdrawal(str(withdrawal_amount)) \
        .wait_for_page_load() \
        .get_message()
    assert withdrawal_message == (
        "Transaction Failed. You can not withdraw amount more than the balance."
    ), "Message after making withdrawal with insufficient balance is incorrect"

