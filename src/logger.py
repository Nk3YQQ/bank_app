import logging
from logging import Logger

from config import LOGGER_PATH

logger_path = LOGGER_PATH


def setup_logger() -> Logger:
    """
    Функция возвращает логгер с установленной конфигурацией для записи логгов в файл
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
        filename=logger_path,
        filemode="w",
    )
    return logging.getLogger()
