import os
from typing import Any

import pandas as pd
import pytest
from dotenv import load_dotenv

from config import TRANSACTIONS_PATH, USER_SETTINGS_PATH
from src.utils import (claim_cards_info, determine_the_interval_of_day, get_info_about_currency, get_info_about_stocks,
                       get_info_about_top_transactions, open_file_with_transactions, open_user_settings)

load_dotenv()

CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")

transactions_path = TRANSACTIONS_PATH
user_settings_path = USER_SETTINGS_PATH


@pytest.fixture
def open_transactions_file_with_date() -> pd.DataFrame:
    return open_file_with_transactions(transactions_path, "20.05.2020")


def test_open_file_with_transactions(open_transactions_file_with_date: pd.DataFrame) -> None:
    assert len(open_file_with_transactions(transactions_path)) == 6705
    transactions = open_transactions_file_with_date.to_dict()
    data_operations = transactions["Дата операции"]
    assert isinstance(data_operations, dict)
    for key, value in data_operations.items():
        assert isinstance(key, int)
        assert isinstance(value, str)


@pytest.mark.parametrize(
    "time, part", [("06:52:17", "утро"), ("12:14:56", "день"), ("20:42:08", "вечер"), ("04:13:29", "ночь")]
)
def test_determine_the_interval_of_day(time: str, part: str) -> None:
    day_part = determine_the_interval_of_day()
    assert day_part in ["утро", "день", "вечер", "ночь"]
    assert determine_the_interval_of_day(time) == part


def test_open_user_settings() -> None:
    user_settings = open_user_settings(user_settings_path)
    assert user_settings == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }


@pytest.fixture
def data() -> Any:
    return open_user_settings(user_settings_path)


def test_get_info_about_currency(data: Any) -> None:
    currencies = get_info_about_currency(data, CURRENCY_API_KEY)
    assert isinstance(currencies, list)
    for currency in currencies:
        assert isinstance(currency, dict)
        assert isinstance(currency["currency"], str)
        assert isinstance(currency["rate"], float)
    currencies = get_info_about_currency(data, "Ключ")
    assert currencies == "Ошибка со стороны программы. Мы быстрее бежим её чинить"
    currencies = get_info_about_currency(data, None)
    assert currencies == "Ошибка. Пустой API"


def test_get_info_about_stocks(data: Any) -> None:
    got_stocks = get_info_about_stocks(data, STOCKS_API_KEY)
    for stock in got_stocks:
        assert stock["stock"] in ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    got_stocks = get_info_about_stocks(data, None)
    assert got_stocks == "Ошибка. Пустой API"


def test_get_info_about_top_transactions(open_transactions_file_with_date: pd.DataFrame) -> None:
    top_transactions = get_info_about_top_transactions(open_transactions_file_with_date)
    assert len(top_transactions) == 5
    for top_transaction in top_transactions:
        assert isinstance(top_transaction, dict)
        assert isinstance(top_transaction["date"], str)
        assert isinstance(top_transaction["amount"], float)
        assert isinstance(top_transaction["category"], str)
        assert isinstance(top_transaction["description"], str)


def test_claim_cards_info(open_transactions_file_with_date: pd.DataFrame) -> None:
    assert claim_cards_info(open_transactions_file_with_date) == [
        {"last_digits": "4556", "total_spent": 1065.0, "cashback": 40.0}
    ]
    transactions = open_file_with_transactions(transactions_path, "20.12.2023")
    assert claim_cards_info(transactions) == []
