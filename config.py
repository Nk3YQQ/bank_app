from pathlib import Path

TRANSACTIONS_PATH = Path(__file__).parent.joinpath("data", "operations.xls")
USER_SETTINGS_PATH = Path(__file__).parent.joinpath("user_settings.json")
RESULT_PATH = Path(__file__).parent.joinpath("data", "result.json")
LOGGER_PATH = Path(__file__).parent.joinpath("data", "mylogs.log")
WRITER_PATH = Path(__file__).parent.joinpath("data", "transactions.json")
