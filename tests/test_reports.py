import pandas as pd
import pytest

from src.reports import spending_by_category
from src.services import open_file_with_all_transactions


@pytest.fixture
def transactions() -> pd.DataFrame:
    return open_file_with_all_transactions("data/operations.xls")


@pytest.mark.parametrize(
    "category, length, expected_result",
    [
        ("Каршеринг", 80, "Каршеринг"),
        ("Дом и ремонт", 13, "Дом и ремонт"),
        ("Местный транспорт", 23, "Местный транспорт"),
    ],
)
def test_spending_by_category(transactions: pd.DataFrame, category: str, length: int, expected_result: str) -> None:
    format_transactions = spending_by_category(transactions, category, "18.12.2021")
    assert len(format_transactions) == length
    for _, transaction in format_transactions.iterrows():
        assert transaction["Категория"] == expected_result
    format_transactions = spending_by_category(transactions, "Без названия")
    assert format_transactions == "По заданному параметру не было найдено не одной транзакции."
