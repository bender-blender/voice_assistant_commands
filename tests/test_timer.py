import pytest
from dependencies.auxiliary_functions import TimeInterval


@pytest.mark.parametrize("text, expected", [
    ("одна секунда", 1),
    ("две минуты", 120),
    ("три часа", 10800),
    ("пять дней", 432000),
    ("десять секунд", 10),
    ("двадцать минут", 1200),
    ("один час двадцать минут", 4800),
    ("одна тысяча секунд", 1000),
    ("три дня пять часов", 259200 + 18000),
])
def test_time_interval_conversion(text, expected):
    time_interval = TimeInterval(text)
    result = time_interval.text_to_number()  # since it's a generator, we get the first yielded value
    assert result == expected