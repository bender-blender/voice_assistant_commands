import pytest
from datetime import datetime
from unittest.mock import patch

from voice_commands.clock.commands.command_date import DateCommands
from voice_commands.models.model_time import TimeModel
from voice_commands.clock.providers.provider_date import call_date
from stark import Response


def test_get_date_returns_timemodel():
    commands = DateCommands()
    result = commands.get_date()
    assert isinstance(result, TimeModel)


def test_formatted_date_format():
    test_date = datetime(year=2025, month=5, day=20)
    model = TimeModel(test_date)
    date_str = model.get_formatted_date()
    assert date_str == "20 мая 2025"


@pytest.mark.asyncio
async def test_call_date_returns_response():
    response = await call_date()
    assert isinstance(response, Response)
    assert isinstance(response.voice, str)


@pytest.mark.asyncio
@patch("voice_commands.clock.helpers.helpers.num2word")
async def test_call_date_contains_words_from_num2word(mock_num2word):
    converted = {}

    def num2word_side_effect(num):
        mapping = {
            1: "один", 2: "два", 3: "три", 4: "четыре", 5: "пять", 6: "шесть",
            7: "семь", 8: "восемь", 9: "девять", 10: "десять", 11: "одиннадцать",
            12: "двенадцать", 13: "тринадцать", 14: "четырнадцать", 15: "пятнадцать",
            16: "шестнадцать", 17: "семнадцать", 18: "восемнадцать", 19: "девятнадцать",
            20: "двадцать", 21: "двадцать один", 22: "двадцать два", 23: "двадцать три",
            24: "двадцать четыре", 25: "двадцать пять", 26: "двадцать шесть",
            27: "двадцать семь", 28: "двадцать восемь", 29: "двадцать девять",
            30: "тридцать", 31: "тридцать один", 2025: "две тысячи двадцать пятый"
        }
        word = mapping.get(num, str(num))
        converted[num] = word
        return word

    mock_num2word.side_effect = num2word_side_effect

    response = await call_date()

    for word in converted.values():
        assert word in response.voice
