from typing import Any

import pandas as pd
import pytest

from config import TRANSACTIONS_PATH, USER_SETTINGS_PATH
from src.utils import (determine_the_interval_of_day, get_info_about_currency, get_info_about_stocks,
                       get_info_about_top_transactions, open_file_with_transactions, open_user_settings)

transactions_path = TRANSACTIONS_PATH
user_settings_path = USER_SETTINGS_PATH


@pytest.fixture
def open_transactions_file_with_date() -> pd.DataFrame:
    transactions = open_file_with_transactions(transactions_path, "20.05.2020")
    return transactions


def test_open_file_with_transactions(open_transactions_file_with_date: pd.DataFrame) -> None:
    assert len(open_file_with_transactions(transactions_path)) == 6705
    transactions = open_transactions_file_with_date.to_dict()
    data_operations = transactions["Дата операции"]
    assert isinstance(data_operations, dict)
    for key, value in data_operations.items():
        assert isinstance(key, int)
        assert isinstance(value, str)


def test_determine_the_interval_of_day() -> None:
    day_part = determine_the_interval_of_day()
    assert day_part in ["утро", "день", "вечер", "ночь"]


def test_open_user_settings() -> None:
    user_settings = open_user_settings(user_settings_path)
    assert user_settings == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }


@pytest.fixture
def data() -> Any:
    user_settings = open_user_settings(user_settings_path)
    return user_settings


def test_get_info_about_currency(data: Any) -> None:
    currencies = get_info_about_currency(data)
    assert isinstance(currencies, list)
    for currency in currencies:
        assert isinstance(currency, dict)
        assert isinstance(currency["currency"], str)
        assert isinstance(currency["rate"], float)


def test_get_info_about_stocks(data: Any) -> None:
    got_stocks = get_info_about_stocks(data)
    for stock in got_stocks:
        assert stock["stock"] in ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def test_get_info_about_top_transactions(open_transactions_file_with_date: pd.DataFrame) -> None:
    top_transactions = get_info_about_top_transactions(open_transactions_file_with_date)
    assert len(top_transactions) == 5
    for top_transaction in top_transactions:
        assert isinstance(top_transaction, dict)
        assert isinstance(top_transaction["date"], str)
        assert isinstance(top_transaction["amount"], float)
        assert isinstance(top_transaction["category"], str)
        assert isinstance(top_transaction["description"], str)
