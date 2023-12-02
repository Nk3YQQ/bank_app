import logging
from logging import Logger


def setup_logger() -> Logger:
    """
    Функция возвращает логгер с установленной конфигурацией для записи логгов в файл
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
        filename="../data/mylogs.log",
        filemode="w",
    )
    return logging.getLogger()
