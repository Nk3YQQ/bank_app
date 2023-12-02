import json

import pandas as pd
import pytest

from src.services import open_file_with_all_transactions, search_the_transaction, search_transactions_to_people


def test_open_file_with_all_transactions() -> None:
    list_of_transactions = open_file_with_all_transactions("data/operations.xls")
    assert len(list_of_transactions) == 6705


@pytest.fixture
def transactions() -> pd.DataFrame:
    return open_file_with_all_transactions("data/operations.xls")


def test_search_the_transaction(transactions: pd.DataFrame) -> None:
    values = ["Колхоз", "", "Здесь нет описания и категории", 1]
    search_descriptions = search_the_transaction(values[0], transactions)
    format_search_descriptions = json.loads(search_descriptions)
    assert len(format_search_descriptions) != 0
    for transaction in format_search_descriptions:
        assert transaction["Описание"] == values[0]
    search_descriptions = search_the_transaction(values[1], transactions)
    assert search_descriptions == "Текст не может быть пустым"
    search_descriptions = search_the_transaction(values[2], transactions)
    format_search_descriptions = json.loads(search_descriptions)
    assert format_search_descriptions == []
    search_descriptions = search_the_transaction(values[3], transactions)
    assert search_descriptions == "Ошибка! Текст не может быть в виде цифры"


@pytest.fixture
def people() -> list[str]:
    return [
        "Сергей П.",
        "Михаил С.",
        "Азер Г.",
        "Людмила Щ.",
        "Владислав Н.",
        "Олеся М.",
        "Сергей З.",
        "Константин Ф.",
        "Дмитрий Ш.",
        "Елена Д.",
        "Татьяна Р.",
        "Степан К.",
        "Сергей Ф.",
        "Егана А.",
        "Светлана Т.",
        "Валерий А.",
        "Екатерина В.",
        "Денис В.",
        "Навид Б.",
        "Кетеван Т.",
        "Дарья И.",
        "Иван С.",
        "Ольга Л.",
        "Виталий Г.",
        "Антон А.",
        "Дмитрий Л.",
        "Владимир Р.",
        "Иван Ф.",
        "Мария Ф.",
        "Андрей Х.",
        "Игорь Б.",
        "Валерий Л.",
        "Вячеслав Ш.",
        "Шахрух Д.",
        "Вероника Э.",
        "Ольга И.",
        "Мария В.",
        "Артем П.",
        "Авазбек К.",
        "Дмитрий Р.",
        "Николай Н.",
        "Ксения К.",
        "Сергей А.",
        "Алексей В.",
        "Никита Ж.",
        "Роза Х.",
        "Игорь С.",
        "Дарья Ч.",
        "Анна Г.",
        "Константин Л.",
        "Наталья Г.",
    ]


def test_search_transactions_to_people(transactions: pd.DataFrame, people: list[str]) -> None:
    searched_transactions = json.loads(search_transactions_to_people(transactions))
    assert len(searched_transactions) == 116
    for transaction in searched_transactions:
        assert transaction["Описание"] in people
