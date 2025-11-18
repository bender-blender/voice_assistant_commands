import pytest
from voice_commands.nl_types.nl_number import NLNumber


@pytest.mark.parametrize('lang, text, expected_value, expected_ordinal', [
    ("en", "42", 42, False),
    ("en", "-7", -7, False),

    # English
    ("en", "seven", 7, False),
    ("en", "forty-two", 42, False),
    ("en", "forty two", 42, False),
    ("en", "minus seven", -7, False),
    ("en", "one thousand two hundred", 1200, False),
    ("en", "twelve hundred", 1200, False),
    ("en", "one million two hundred thirty four thousand five hundred sixty seven", 1234567, False),
    # Fractions
    ("en", "three point one four", 3.14, False),
    ("en", "one half", 0.5, False),
    ("en", "two and half", 2.5, False),
    ("en", "a quarter", 0.25, False),
    ("en", "one quarter", 0.25, False),
    ("en", "three quarters", 0.75, False),
    ("en", "minus three quarters", -0.75, False),
    # Ordinal
    ("en", "first", 1, True),
    ("en", "twenty-third", 23, True),
    ("en", "twenty third", 23, True),

    # Russian
    ("ru", "сорок два", 42, False),
    ("ru", "семь", 7, False),
    ("ru", "одна тысяча двести", 1200, False),
    ("ru", "тридцать пять тысяч", 35000, False),
    ("ru", "один миллион двести тридцать четыре тысячи пятьсот шестьдесят семь", 1234567, False),
    # Decimals
    ("ru", "три целых четырнадцать сотых", 3.14, False),
    ("ru", "три точка четырнадцать", 3.14, False),
    ("ru", "один и шесть", 1.6, False),
    ("ru", "два целых пять десятых", 2.5, False),
    # Fractions
    ("ru", "полтора", 1.5, False),
    ("ru", "половина", 0.5, False),
    ("ru", "четверть", 0.25, False),
    ("ru", "три четверти", 0.75, False),
    ("ru", "две трети", round(2/3,2), False),
    ("ru", "четырнадцать сотых", 0.14, False),
    ("ru", "пять десятых", 0.5, False),
    ("ru", "пять сотых", 0.05, False),
    ("ru", "пять двадцатых", round(5/20,2), False),
    ("ru", "одна вторая", 0.5, False),
    ("ru", "минус три четверти", -0.75, False),
    # Ordinals
    ("ru", "первый", 1, True),
    ("ru", "двадцать третий", 23, True),
    # Negative numbers
    ("ru", "минус семь", -7, False),

    # Test Extraction (English)
    ("en", "I have two point five apples", 2.5, False),
    ("en", "She finished twenty-third in the race", 23, True),
    ("en", "He owes me three quarters of a dollar", 0.75, False),
])
@pytest.mark.asyncio
async def test_nlnumber_parse(lang, text, expected_value, expected_ordinal):
    nl_number = NLNumber(None)
    b = await nl_number.did_parse(text)
    print(b)
    assert nl_number.value == expected_value
    assert nl_number.is_ordinal == expected_ordinal
