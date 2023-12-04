import json
import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.utils import (claim_cards_info, determine_the_interval_of_day, get_info_about_currency, get_info_about_stocks,
                       get_info_about_top_transactions, open_file_with_transactions, open_user_settings)

logger = logging.getLogger(__name__)

load_dotenv()

CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")


def views(
    data: str,
    result_filepath: Path,
    transactions_filepath: Path,
    user_settings_filepath: Path,
) -> dict | Any:
    """
    Функция реализует веб-страницу в формате json, а также записывает данные в файл 'result.json'
    """
    try:
        transactions = open_file_with_transactions(transactions_filepath, data)
        user_settings = open_user_settings(user_settings_filepath)
        part_of_day = determine_the_interval_of_day()
        cards_info = claim_cards_info(transactions)
        top_transactions = get_info_about_top_transactions(transactions)
        currency_info = get_info_about_currency(user_settings, CURRENCY_API_KEY)
        stocks_info = get_info_about_stocks(user_settings, STOCKS_API_KEY)
        web_page = {
            "greeting": f"Добрый {part_of_day}",
            "cards": cards_info,
            "top_transactions": top_transactions,
            "currency_rates": currency_info,
            "stock_prices": stocks_info,
        }
        with open(result_filepath, "w", encoding="utf-8") as file:
            json.dump(web_page, file, indent=4, ensure_ascii=False)

        return web_page
    except (ValueError, TypeError) as e:
        logger.error(f"views error:{e}")
        return "Ошибка! Неверно указана дата"
