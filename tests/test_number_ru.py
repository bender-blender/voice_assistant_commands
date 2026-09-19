import pytest

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumberRU


@pytest.mark.parametrize(
    "text, expected_value, expected_ordinal",
    [
        # Normal numbers
        ("сорок два", 42, False),
        ("семь", 7, False),
        ("одна тысяча двести", 1200, False),
        ("тридцать пять тысяч", 35000, False),
        (
            "один миллион двести тридцать четыре тысячи "
            "пятьсот шестьдесят семь",
            1234567,
            False,
        ),
        ("пять", 5, False),
        ("сорок пять", 45, False),
        ("сто сорок пять", 145, False),
        ("тысяча пятьсот сорок два", 1542, False),

        # Take the first number
        ("двадцать десять", 20, False),
        ("сто сто", 100, False),
        ("сто пятьдесят сорок", 150, False),

        # Ordinals
        ("первый", 1, True),
        ("второй", 2, True),
        ("третий", 3, True),
        ("пятый", 5, True),
        ("двадцать первый", 21, True),
        ("двадцать третий", 23, True),
        ("тридцать второй", 32, True),
        ("сто двадцать третий", 123, True),

        # Fractions
        ("полтора", 1.5, False),
        ("половина", 0.5, False),
        ("четверть", 0.25, False),
        ("одна вторая", 0.5, False),
        ("две трети", 2 / 3, False),
        ("три четверти", 3 / 4, False),
        ("пять десятых", 5 / 10, False),
        ("пять сотых", 5 / 100, False),
        ("семь сотых", 7 / 100, False),
        ("семь тысячных", 7 / 1000, False),
        ("четырнадцать сотых", 14 / 100, False),
        ("пять двадцатых", 5 / 20, False),

        # Standalone denominator forms
        ("вторых", 1 / 2, False),
        ("третьих", 1 / 3, False),
        ("четвертых", 1 / 4, False),
        ("пятых", 1 / 5, False),

        # Compound denominators
        ("тринадцать тридцать пятых", 13 / 35, False),
        ("пять двадцать пятых", 5 / 25, False),
        ("семь сорок пятых", 7 / 45, False),
        ("девять сто двадцать пятых", 9 / 125, False),

        # Mixed fractions
        ("три целых четырнадцать сотых", 3.14, False),
        ("одна целая пять десятых", 1.5, False),
        ("два целых пять десятых", 2.5, False),
        ("две целых три четверти", 2.75, False),
        ("ноль целых семь сотых", 0.07, False),

        # Decimal point
        ("три точка четырнадцать", 3.14, False),
        ("ноль точка пять", 0.5, False),
        ("пять точка ноль пять", 5.05, False),
        ("пять точка ноль ноль пять", 5.005, False),
        ("ноль точка ноль семь", 0.07, False),

        # Negative values
        ("минус семь", -7, False),
        ("минус пять", -5, False),
        ("минус пятый", -5, True),
        ("минус три четверти", -3 / 4, False),
        ("минус две трети", -2 / 3, False),
        ("минус четверть", -1 / 4, False),
        ("минус три точка четырнадцать", -3.14, False),
        ("минус одна целая одна вторая", -1.5, False),

        # Sentences
        ("поставь будильник на пять", 5, False),
        ("напомни мне через сорок пять минут", 45, False),
        ("температура сто сорок пять градусов", 145, False),
        ("купи двести тридцать семь яблок", 237, False),
        (
            "поставь таймер на пять минут через десять секунд",
            5,
            False,
        ),
        (
            "через сорок пять минут напомни про сто рублей",
            45,
            False,
        ),
        (
            "закажи пять двадцать пятых килограмма сахара",
            5 / 25,
            False,
        ),
        (
            "температура минус две целых пять десятых градуса",
            -2.5,
            False,
        ),
    ],
)
@pytest.mark.asyncio
async def test_nlnumber_ru_parse(
    text,
    expected_value,
    expected_ordinal,
):
    parse = await pattern_parser.parse_object(
        NLNumberRU,
        text,
    )

    assert parse.obj.value == pytest.approx(
        expected_value,
    )

    assert (
        parse.obj.is_ordinal
        == expected_ordinal
    )