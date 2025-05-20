import pytest
from datetime import datetime
from unittest.mock import patch

from voice_commands.clock.commands.command_clock import TimeCommands
from voice_commands.models.model_time import TimeModel
from voice_commands.clock.providers.provider_time import call_time
from stark import Response


def test_get_time_returns_timemodel():
    commands = TimeCommands()
    result = commands.get_time()
    assert isinstance(result, TimeModel)


def test_formatted_time_format():
    test_time = datetime(year=2025, month=1, day=1, hour=7, minute=30)
    model = TimeModel(test_time)
    time_str = model.get_formatted_time()
    assert time_str == "07:30"


@pytest.mark.asyncio
async def test_call_time_returns_response():
    response = await call_time()
    assert isinstance(response, Response)
    assert isinstance(response.voice, str)

@pytest.mark.asyncio
@patch("voice_commands.clock.helpers.helpers.num2word")
async def test_call_time_contains_words_from_num2word(mock_num2word):
    converted = {}

    def num2word_side_effect(num):
        words = {
        0: "ноль", 1: "один", 2: "два", 3: "три", 4: "четыре", 5: "пять",
        6: "шесть", 7: "семь", 8: "восемь", 9: "девять", 10: "десять",
        11: "одиннадцать", 12: "двенадцать", 13: "тринадцать", 14: "четырнадцать",
        15: "пятнадцать", 16: "шестнадцать", 17: "семнадцать", 18: "восемнадцать",
        19: "девятнадцать", 20: "двадцать", 21: "двадцать один", 22: "двадцать два",
        23: "двадцать три", 24: "двадцать четыре", 25: "двадцать пять", 
        26: "двадцать шесть", 27: "двадцать семь", 28: "двадцать восемь", 
        29: "двадцать девять", 30: "тридцать", 31: "тридцать один", 
        32: "тридцать два", 33: "тридцать три", 34: "тридцать четыре",
        35: "тридцать пять", 36: "тридцать шесть", 37: "тридцать семь", 
        38: "тридцать восемь", 39: "тридцать девять", 40: "сорок", 
        41: "сорок один", 42: "сорок два", 43: "сорок три", 44: "сорок четыре",
        45: "сорок пять", 46: "сорок шесть", 47: "сорок семь", 48: "сорок восемь",
        49: "сорок девять", 50: "пятьдесят", 51: "пятьдесят один", 52: "пятьдесят два",
        53: "пятьдесят три", 54: "пятьдесят четыре", 55: "пятьдесят пять", 
        56: "пятьдесят шесть", 57: "пятьдесят семь", 58: "пятьдесят восемь",
        59: "пятьдесят девять"
    }
        word = words.get(num, str(num))
        converted[num] = word
        return word

    mock_num2word.side_effect = num2word_side_effect

    response = await call_time()

    for word in converted.values():
        assert word in response.voice