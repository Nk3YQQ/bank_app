import logging

from src.logger import setup_logger
from src.views import views
from src.services import open_file_with_all_transactions, search_the_transaction, search_transactions_to_people
from src.reports import spending_by_category

logger = setup_logger()

if __name__ == "__main__":
    while True:
        user_input = input('Чтобы посмотреть данные о транзакциях, нажмите "1". Чтобы выйти, '
                           'нажмите "3": ')
        if user_input == "1":
            user_input_date = input('Введите дату в формате 21.12.2021: ')
            print(views(user_input_date))
            if views(user_input_date) == 'Ошибка! Неверно указана дата':
                continue
            user_input = input('Если Вы хотите найти транзакцию по категории, нажмите "1", Если Вы хотите найти '
                               'транзакции физ. лицам, нажмите "2": ')
            transactions = open_file_with_all_transactions()
            if user_input == "1":
                user_input_category = input('Введите категорию транзакции, которую хотите посмотреть: ')
                print(search_the_transaction(user_input_category, transactions))
                if search_the_transaction(user_input_category, transactions) == 'Такая категория не найдена':
                    continue
            elif user_input == "2":
                print(search_transactions_to_people(transactions))
            else:
                print('Неправильно введённая команда!')
                continue
            user_input = input('Если Вы хотите посмотреть Ваши траты по заданной категории за последние 3 месяца и '
                               'сформировать отчёт, нажмите "1". Если выйти - нажмите "3": ')
            if user_input == "1":
                user_input_category = input('Введите категорию транзакции, которую хотите посмотреть: ')
                print(spending_by_category(transactions, user_input_category, user_input_date))

            elif user_input == "3":
                break
            else:
                print('Неправильно введённая команда!')
                continue

            user_input = input('Подскажите, хотите ли Вы продолжить или Вы хотите выйти? Нажмите "3", если хотите '
                               'выйти или "1", если хотите остаться: ')
            if user_input == "3":
                break
            elif user_input == "1":
                continue
            else:
                print('Неправильно введённая команда!')

        elif user_input == "3":
            break
        else:
            print('Неправильно введённая команда!')
            continue
