import json
import os
from datetime import datetime
from typing import Any, Hashable

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")


def open_file_with_transactions(date: str, filepath: str = "../data/operations.xls") -> pd.DataFrame:
    """
    Функция читает файл и возвращает список, в котором хранятся транзакции
    """
    transactions = pd.read_excel(filepath)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
    format_date = pd.to_datetime(date, format="%d.%m.%Y")
    start_date = pd.to_datetime(f"01.{format_date.month}.{format_date.year}", format="%d.%m.%Y")
    sorted_transactions_by_date = transactions.loc[
        (transactions["Дата платежа"] <= date) & (transactions["Дата платежа"] >= start_date)
    ]
    return sorted_transactions_by_date


def determine_the_interval_of_day() -> str:
    """
    Функция определяет какое сейчас время и возвращает промежуток дня: утро, день, вечер или ночь
    """
    time = datetime.now().strftime("%H:%M:%S")
    if 5 <= int(time[0:2]) < 11:
        return "утро"
    elif 11 <= int(time[0:2]) < 17:
        return "день"
    elif 17 <= int(time[0:2]) < 23:
        return "вечер"
    else:
        return "ночь"


def open_user_settings(filepath: str = "../user_settings.json") -> Any:
    """
    Функция открывает и читает файл, содержащий пользовательские настройки
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def get_info_about_currency(user_settings: Any) -> Any:
    """
    Функция возвращает список с курсами доллар/рубль, евро/рубль и юань/рубль
    """
    if CURRENCY_API_KEY is None:
        return "Ошибка. Пустой API"
    got_currencies: list = []
    currencies = user_settings["user_currencies"]
    for currency in currencies:
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
        response = requests.get(url, headers={"apikey": CURRENCY_API_KEY})
        response_data = json.loads(response.content)
        got_currency = {"currency": currency, "rate": round(response_data["rates"]["RUB"], 2)}
        got_currencies.append(got_currency)
    return got_currencies


def get_info_about_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """
    Функция принимает список транзакций и возвращает список словарей о топ 5 переводов за месяц
    """
    top_transactions: list = []
    grouped_transactions = transactions.sort_values("Сумма операции с округлением", ascending=False)
    for _, row in grouped_transactions.iterrows():
        top_transaction = {
            "date": row["Дата платежа"].strftime("%d.%m.%Y"),
            "amount": row["Сумма операции с округлением"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        top_transactions.append(top_transaction)
        if len(top_transactions) == 5:
            break
    return top_transactions


def get_info_about_stocks(user_settings: Any) -> list[dict] | Any:
    """
    Функция возвращает словарь с пятью рандомными компаниями с указанной ценой
    """
    if STOCKS_API_KEY is None:
        return "Ошибка. Пустой API"
    got_stocks: list = []
    user_stocks = user_settings["user_stocks"]
    for stock in user_stocks:
        url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={STOCKS_API_KEY}"
        response = requests.get(url)
        response_data = json.loads(response.content)
        got_stock = {"stock": stock, "price": response_data["c"]}
        got_stocks.append(got_stock)
    return got_stocks


def claim_cards_info(transactions: pd.DataFrame) -> list[dict] | Any:
    """
    Функция возвращает информацию о карте, общих трат и кешбэке
    """
    cards_info: list = []
    cards_grouped = transactions.groupby("Номер карты")
    sorted_by_card_and_total_spent = cards_grouped.agg({"Сумма операции с округлением": "sum", "Кэшбэк": "sum"})
    for card_number, row in sorted_by_card_and_total_spent.iterrows():
        if isinstance(card_number, Hashable):
            return "Ошибка!"
        reformat_card_number = card_number[1:5]
        total_spent = row["Сумма операции с округлением"]
        cashback = row["Кэшбэк"]
        card_info = {
            "last_digits": reformat_card_number,
            "total_spent": round(float(total_spent), 2),
            "cashback": round(float(cashback), 2),
        }
        cards_info.append(card_info)
    return cards_info
