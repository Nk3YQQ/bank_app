import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd

from config import WRITER_PATH

logger = logging.getLogger(__name__)

writer_path = WRITER_PATH


def writing_to_file(filepath: Path) -> Callable[..., Any]:
    """
    Декоратор записывает полученные данные из функции в файл-отчёт в формате json
    """

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            if isinstance(result, str):
                logger.error("writing_to_file error: got str, not dataframe")
                return result
            list_of_transactions = []
            for _, transaction in result.iterrows():
                transaction_params = {
                    "date": transaction["Дата платежа"].strftime("%d.%m.%Y"),
                    "amount": transaction["Сумма операции с округлением"],
                    "category": transaction["Категория"],
                    "description": transaction["Описание"],
                }
                list_of_transactions.append(transaction_params)
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(list_of_transactions, file, indent=4, ensure_ascii=False)
            logger.info("writing_to_file is working. Status: ok")
            return result

        return inner

    return decorator


@writing_to_file(writer_path)
def spending_by_category(
    transactions: pd.DataFrame, category_name: str, date: Optional[str] = None
) -> pd.DataFrame | str:
    """
    Функция возвращает траты по заданной категории за последние 3 месяца
    """
    if not date:
        date = datetime.now().strftime("%d.%m.%Y")
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    format_date = pd.to_datetime(date, format="%d.%m.%Y")
    start_date = pd.to_datetime(f"{format_date.day}.{format_date.month - 3}.{format_date.year}", format="%d.%m.%Y")
    sorted_transactions = transactions[transactions["Категория"].str.contains(category_name, case=False, na=False)]
    sorted_transactions_by_date = sorted_transactions.loc[
        (sorted_transactions["Дата платежа"] <= date) & (sorted_transactions["Дата платежа"] >= start_date)
    ]
    if len(sorted_transactions) == 0:
        logger.error("spending_by_category: no such date in file")
        return "По заданному параметру не было найдено не одной транзакции."
    logger.info("spending_by_category is working. Status: ok")
    return sorted_transactions_by_date
