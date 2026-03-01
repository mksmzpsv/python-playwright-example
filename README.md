# Python Playwright Example

End-to-end test automation for the [GlobalsQA XYZ Bank app](https://www.globalsqa.com/angularJs-protractor/BankingProject/#/) demo app using **Python**, **Playwright**, and **pytest**.

## Project Setup

### Prerequisites

- Python 3.12+
- [Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline) (optional, for viewing reports)

### Installation

```sh
# Clone the repository
git clone https://github.com/mksmzpsv/python-playwright-example.git
cd python-playwright-example

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

> **Tip:** Set the `BASE_URL` environment variable to override the default target URL:
>
> ```sh
> export BASE_URL="http://localhost:8080"
> ```

## Running Tests

```sh
# Run all tests
pytest

# Run a single test file
pytest src/tests/customer_tests.py
```

### Different Browsers

The default browser is Chromium (from the default Playwright configuration). Override with `--browser`:

```sh
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# Run against multiple browsers in one session
pytest --browser chromium --browser firefox --browser webkit
```

### Headed Mode & Slow Motion

```sh
pytest --headed
pytest --headed --slowmo 500
```

### Parallel Execution

Tests can run in parallel using `pytest-xdist` (included in dependencies):

```sh
# Run tests across 4 workers
pytest -n 4

# Auto-detect number of CPU cores
pytest -n auto
```

All [pytest-playwright CLI options](https://playwright.dev/python/docs/test-runners#cli-arguments) are supported.

## Allure Reports

Test results are written to `allure-results/` automatically. On failure, screenshots, videos, and traces are attached to the report.

```sh
# View the report
allure serve allure-results
```

## Features

- **Page Object Model** — every page extends `BasePage`; reusable generic `DropdownComponent` and `TableComponent` for `<select>` elements and HTML tables.
- **Pytest fixtures** — return page objects for clean test setup (`login_as_specific_customer`, `open_select_customer_page`, `login_as_bank_manager`, `add_customer`).
- **Typed data models** — dataclasses (`CustomerAccountInfo`, `TransactionInfo`, `CustomerInfo`) with factory methods for parsing UI text.
- **Allure integration** — automatic artifact attachment (screenshots / video / traces) on failure via a `conftest.py` hook.

## Project Structure

```
conftest.py                        # Global pytest fixtures and hooks
pyproject.toml                     # Project metadata & pytest configuration
requirements.txt                   # Pinned dependencies
src/
  fixtures/                        # Pytest custom fixtures
  testdata/                        # Dataclasses models for test data
  pages/                           # Page Objects
    components/                    # Generic reusable Page Component Objects
    customer/
    bank_manager/
  tests/                           # Tests
```
