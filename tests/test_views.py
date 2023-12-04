import pytest

from config import RESULT_PATH, TRANSACTIONS_PATH, USER_SETTINGS_PATH
from src.views import views

transactions_path = TRANSACTIONS_PATH
user_settings_path = USER_SETTINGS_PATH
result_path = RESULT_PATH


@pytest.mark.parametrize(
    "data, expected_result", [("20.05.2020", True), ("21.07.2020", True), ("20-05-2020", False), ("20.01.2023", True)]
)
def test_views(data: str, expected_result: bool) -> None:
    web_page = views(data, result_path, transactions_path, user_settings_path)
    assert isinstance(web_page, dict) == expected_result
