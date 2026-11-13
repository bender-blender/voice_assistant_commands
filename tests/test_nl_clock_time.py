import pytest

from voice_commands.nl_types.parsing_context import pattern_parser
from clock import NLClockTime, Clock


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Без части суток -> pm=None
        ("час", Clock(1, 0, None)),
        ("два часа", Clock(2, 0, None)),
        ("шесть", Clock(6, 0, None)),
        ("шесть часов", Clock(6, 0, None)),
        ("одиннадцать", Clock(11, 0, None)),
        ("в шесть", Clock(6, 0, None)),
        ("в одиннадцать часов", Clock(11, 0, None)),
        ("шесть тридцать", Clock(6, 30, None)),
        ("пять часов пятнадцать", Clock(5, 15, None)),

        # Утро
        ("час утра", Clock(1, 0, True)),
        ("два часа утра", Clock(2, 0, True)),
        ("шесть утра", Clock(6, 0, True)),
        ("шесть часов утра", Clock(6, 0, True)),
        ("одиннадцать утра", Clock(11, 0, True)),

        # День
        ("час дня", Clock(1, 0, False)),
        ("два часа дня", Clock(2, 0, False)),
        ("шесть часов дня", Clock(6, 0, False)),
        ("одиннадцать дня", Clock(11, 0, False)),

        # Вечер
        ("час вечера", Clock(1, 0, False)),
        ("пять вечера", Clock(5, 0, False)),
        ("шесть часов вечера", Clock(6, 0, False)),
        ("одиннадцать вечера", Clock(11, 0, False)),

        # Ночь
        ("час ночи", Clock(1, 0, False)),
        ("три часа ночи", Clock(3, 0, False)),
        ("шесть ночи", Clock(6, 0, False)),

        # С минутами и частью суток
        ("шесть часов пятнадцать утра", Clock(6, 15, True)),
        ("пять часов тридцать вечера", Clock(5, 30, False)),
        ("одиннадцать часов сорок пять вечера", Clock(11, 45, False)),

        # С "в"
        ("в шесть утра", Clock(6, 0, True)),
        ("в час дня", Clock(1, 0, False)),
        ("в пять вечера", Clock(5, 0, False)),
        ("в три часа ночи", Clock(3, 0, False)),
    ],
)
async def test_nl_clock_with_day_part(text, expected):
    result = await pattern_parser.parse_object(
        NLClockTime,
        text,
    )

    assert result.obj.value == expected
    assert str(result.substring) == text