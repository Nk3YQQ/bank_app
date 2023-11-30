import pytest

from src.views import views


@pytest.mark.parametrize(
    "data, expected_result", [("20.05.2020", True), ("21.07.2020", True), ("20-05-2020", False), ("20.01.2023", True)]
)
def test_views(data: str, expected_result: bool) -> None:
    web_page = views(data)
    assert isinstance(web_page, dict) == expected_result
