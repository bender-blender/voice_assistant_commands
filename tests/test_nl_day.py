import pytest

from stark.core.parsing import ParseError

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_day import NLDay


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected", "substring"),
    [
        # Russian
        ("первого", 1, "первого"),
        ("второго", 2, "второго"),
        ("третьего", 3, "третьего"),
        ("пятого", 5, "пятого"),
        ("десятого", 10, "десятого"),
        ("одиннадцатого", 11, "одиннадцатого"),
        ("пятнадцатого", 15, "пятнадцатого"),
        ("двадцатого", 20, "двадцатого"),
        ("двадцать пятого", 25, "двадцать пятого"),
        ("тридцать первого", 31, "тридцать первого"),

        # Russian + "числа"
        ("пятого числа", 5, "пятого числа"),
        ("двадцать первого числа", 21, "двадцать первого числа"),

        # Внутри предложения
        ("пятого сентября", 5, "пятого"),
        ("встреча десятого октября", 10, "десятого"),

        # English
        ("first", 1, "first"),
        ("fifth", 5, "fifth"),
        ("tenth", 10, "tenth"),
        ("twenty first", 21, "twenty first"),
        ("on the fifth", 5, "on the fifth"),
        ("on the twenty fifth", 25, "on the twenty fifth"),
    ],
)
async def test_nl_day(text, expected, substring):
    result = await pattern_parser.parse_object(
        NLDay,
        text,
    )

    assert result.obj.value == expected
    assert str(result.substring) == substring


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "пять",
        "десять",
        "двадцать",
        "двадцать пять",
        "тридцать один",
        "five",
        "ten",
        "twenty",
        "twenty five",
        "thirty one",
    ],
)
async def test_nl_day_rejects_cardinal_numbers(text):
    with pytest.raises(ParseError):
        await pattern_parser.parse_object(
            NLDay,
            text,
        )