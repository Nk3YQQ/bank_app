import json
import logging
from typing import Any

from src.utils import (claim_cards_info, determine_the_interval_of_day, get_info_about_currency, get_info_about_stocks,
                       get_info_about_top_transactions, open_file_with_transactions, open_user_settings)

logger = logging.getLogger(__name__)


def views(
    data: str,
    filepath: str = "../data/result.json",
    transactions_filepath: str = "../data/operations.xls",
    user_settings_filepath: str = "../user_settings.json",
) -> dict | Any:
    """
    Функция реализует веб-страницу в формате json, а также записывает данные в файл 'result.json'
    """
    try:
        transactions = open_file_with_transactions(data, transactions_filepath)
        user_settings = open_user_settings(user_settings_filepath)
        part_of_day = determine_the_interval_of_day()
        cards_info = claim_cards_info(transactions)
        top_transactions = get_info_about_top_transactions(transactions)
        currency_info = get_info_about_currency(user_settings)
        stocks_info = get_info_about_stocks(user_settings)
        web_page = {
            "greeting": f"Добрый {part_of_day}",
            "cards": cards_info,
            "top_transactions": top_transactions,
            "currency_rates": currency_info,
            "stock_prices": stocks_info,
        }
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(web_page, file, indent=4, ensure_ascii=False)

        return web_page
    except (ValueError, TypeError) as e:
        logger.error(f"views error:{e}")
        return "Ошибка! Неверно указана дата"
