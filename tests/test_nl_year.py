import pytest

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_year import (
    NLYear,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Russian
        ("двадцать пять", 2025),
        ("двадцать шесть", 2026),
        ("двадцать семь", 1927),
        ("восемьдесят девять", 1989),
        ("двадцать пять год", 2025),
        ("тысяча девятьсот восемьдесят девять", 1989),
        ("две тысячи двадцать", 2020),
        ("две тысячи двадцать пять", 2025),

        # English
        ("twenty five", 2025),
        ("twenty six", 2026),
        ("twenty seven", 1927),
        ("eighty nine", 1989),
        ("twenty five year", 2025),

        # English year notation
        ("nineteen eighty", 1980),
        ("nineteen eighty nine", 1989),
        ("nineteen eighty nine", 1989),
        ("nineteen ninety nine", 1999),
        ("twenty twenty", 2020),
        ("twenty twenty five", 2025),
        ("the year nineteen eighty nine", 1989),
    ],
)
async def test_nl_year(
    text: str,
    expected: int,
):
    result = await pattern_parser.parse_object(
        NLYear,
        text,
    )

    assert result.obj.value == expected, (
        f"\n"
        f"text={text!r}\n"
        f"value={result.obj.value!r}\n"
        f"expected={expected!r}\n"
        f"year={result.obj.year!r}\n"
        f"year_part={getattr(result.obj, 'year_part', None)!r}\n"
        f"century={result.obj.century!r}\n"
        f"substring={result.substring!r}"
    )