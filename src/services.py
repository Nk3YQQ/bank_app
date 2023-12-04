import json
import logging
import re
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def search_the_transaction(search_text: str | Any, transactions: pd.DataFrame) -> str:
    """
    Функция принимает строку поиска и возвращает вск транзакции,
    содержащие данный текст в описании или в категории
    """
    try:
        if not search_text:
            return "Текст не может быть пустым"
        found_transactions = transactions[
            transactions["Описание"].str.contains(search_text, case=False)
            | transactions["Категория"].str.contains(search_text, case=False)
        ].to_dict(orient="records")

        logger.info("search_the_transaction is working. Status: ok")
        if not found_transactions:
            return "[]"
        return json.dumps(found_transactions, ensure_ascii=False)

    except (ValueError, AttributeError, TypeError) as e:
        logger.error(f"get_transaction error:{e}")
        return "Ошибка! Текст не может быть в виде цифры"


def search_transactions_to_people(transactions: pd.DataFrame) -> str:
    """
    Функция возвращает json со всеми транзакциями, которые про перевод физическим лицам.
    """
    pattern = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$")
    list_of_transactions: list = []
    for _, row in transactions.iterrows():
        category = row["Категория"]
        description = row["Описание"]
        if category == "Переводы" and pattern.match(description):
            list_of_transactions.append(row.to_dict())
    logger.info("search_transactions_to_people is working. Status: ok")
    return json.dumps(list_of_transactions, ensure_ascii=False)
