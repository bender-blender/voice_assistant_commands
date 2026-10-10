import pytest
from datetime import datetime

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_calendar_date import (
    NLCalendarDate,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Russian — full date
        ("пятого сентября две тысячи двадцать пять", "05.09.2025"),
        ("первого января две тысячи двадцать", "01.01.2020"),
        ("десятого октября две тысячи двадцать четыре", "10.10.2024"),
        ("двадцать пятого декабря две тысячи двадцать три", "25.12.2023"),
        ("тридцатого июня две тысячи двадцать два", "30.06.2022"),

        # English — full date
        ("fifth september twenty twenty five", "05.09.2025"),
        ("first january twenty twenty", "01.01.2020"),
        ("tenth october twenty twenty four", "10.10.2024"),
        ("twenty fifth december twenty twenty three", "25.12.2023"),
        ("thirtieth june twenty twenty two", "30.06.2022"),
    ],
)
async def test_calendar_date_full(
    text: str,
    expected: str,
):
    result = await pattern_parser.parse_object(
        NLCalendarDate,
        text,
    )

    assert result.obj.value == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "day", "month"),
    [
        # Russian — without year
        ("пятого сентября", 5, 9),
        ("первого января", 1, 1),
        ("десятого октября", 10, 10),
        ("двадцать пятого декабря", 25, 12),
        ("тридцатого июня", 30, 6),

        # English — without year
        ("fifth september", 5, 9),
        ("first january", 1, 1),
        ("tenth october", 10, 10),
        ("twenty fifth december", 25, 12),
        ("thirtieth june", 30, 6),
    ],
)
async def test_calendar_date_without_year(
    text: str,
    day: int,
    month: int,
):
    result = await pattern_parser.parse_object(
        NLCalendarDate,
        text,
    )

    current_year = datetime.now().year

    expected = (
        f"{day:02d}."
        f"{month:02d}."
        f"{current_year}"
    )

    assert result.obj.value == expected