from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class CustomerAccountInfo:
    ACCOUNT_NUMBER_KEY: ClassVar[str] = "Account Number"
    BALANCE_KEY: ClassVar[str] = "Balance"
    CURRENCY_KEY: ClassVar[str] = "Currency"

    number: str
    balance: int
    currency: str

    @classmethod
    def from_raw_text(cls, raw_text: str) -> CustomerAccountInfo:
        normalized = raw_text.replace("\n", "").replace("\t", "")
        pairs = normalized.split(",")
        data: dict[str, str] = {}
        for pair in pairs:
            key, value = pair.split(":", 1)
            data[key.strip()] = value.strip()
        return cls(
            number=data.get(cls.ACCOUNT_NUMBER_KEY, ""),
            balance=int(data.get(cls.BALANCE_KEY, 0)),
            currency=data.get(cls.CURRENCY_KEY, ""),
        )


@dataclass
class TransactionInfo:
    DATE_TIME_KEY: ClassVar[str] = "Date-Time"
    AMOUNT_KEY: ClassVar[str] = "Amount"
    TRANSACTION_TYPE_KEY: ClassVar[str] = "Transaction Type"

    date_time: str
    amount: int
    transaction_type: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> TransactionInfo:
        return cls(
            date_time=data.get(cls.DATE_TIME_KEY, ""),
            amount=int(data.get(cls.AMOUNT_KEY, 0)),
            transaction_type=data.get(cls.TRANSACTION_TYPE_KEY, ""),
        )


@dataclass
class CustomerInfo:
    FIRST_NAME_KEY: ClassVar[str] = "First Name"
    LAST_NAME_KEY: ClassVar[str] = "Last Name"
    POST_CODE_KEY: ClassVar[str] = "Post Code"
    ACCOUNT_NUMBER_KEY: ClassVar[str] = "Account Number"

    first_name: str
    last_name: str
    post_code: str
    account_number: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> CustomerInfo:
        return cls(
            first_name=data.get(cls.FIRST_NAME_KEY, ""),
            last_name=data.get(cls.LAST_NAME_KEY, ""),
            post_code=data.get(cls.POST_CODE_KEY, ""),
            account_number=data.get(cls.ACCOUNT_NUMBER_KEY, ""),
        )
