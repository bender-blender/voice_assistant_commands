import pytest

from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_clock import (
    NLClokTime,
)
from voice_commands.nl_types.parsing_context import pattern_parser


async def check_time(text: str, expected: str):
    result = await pattern_parser.parse_object(
        NLClokTime,
        text,
    )

    assert result.obj.value == expected, (
        f"\n"
        f"text={text!r}\n"
        f"value={result.obj.value!r}\n"
        f"expected={expected!r}\n"
        f"substring={result.substring!r}"
    )


# ============================================================
# STAGE 1
# x y
# ============================================================

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Russian
        ("один пять", "01:05"),
        ("два десять", "02:10"),
        ("три пятнадцать", "03:15"),
        ("четыре двадцать", "04:20"),
        ("пять двадцать пять", "05:25"),
        ("шесть тридцать", "06:30"),
        ("семь тридцать пять", "07:35"),
        ("восемь сорок", "08:40"),
        ("девять сорок пять", "09:45"),
        ("десять пятьдесят", "10:50"),

        # English
        ("one five", "01:05"),
        ("two ten", "02:10"),
        ("three fifteen", "03:15"),
        ("four twenty", "04:20"),
        ("five twenty five", "05:25"),
        ("six thirty", "06:30"),
        ("seven thirty five", "07:35"),
        ("eight forty", "08:40"),
        ("nine forty five", "09:45"),
        ("twelve thirty six", "12:36"),
    ],
)
async def test_clock_time_stage_1(
    text: str,
    expected: str,
):
    await check_time(text, expected)


# ============================================================
# STAGE 2
# x hours y minutes
# ============================================================

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Russian
        ("один час одна минута", "01:01"),
        ("два часа пять минут", "02:05"),
        ("три часа десять минут", "03:10"),
        ("четыре часа пятнадцать минут", "04:15"),
        ("пять часов двадцать минут", "05:20"),
        ("шесть часов двадцать пять минут", "06:25"),
        ("семь часов тридцать минут", "07:30"),
        ("восемь часов тридцать пять минут", "08:35"),
        ("девять часов сорок пять минут", "09:45"),
        (
            "двенадцать часов пятьдесят девять минут",
            "12:59",
        ),

        # English
        ("one hour one minute", "01:01"),
        ("two hours five minutes", "02:05"),
        ("three hours ten minutes", "03:10"),
        ("four hours fifteen minutes", "04:15"),
        ("five hours twenty minutes", "05:20"),
        ("six hours twenty five minutes", "06:25"),
        ("seven hours thirty minutes", "07:30"),
        ("eight hours thirty five minutes", "08:35"),
        ("nine hours forty five minutes", "09:45"),
        (
            "twelve hours fifty nine minutes",
            "12:59",
        ),
    ],
)
async def test_clock_time_stage_2(
    text: str,
    expected: str,
):
    await check_time(text, expected)


# ============================================================
# STAGE 3
# x hours
# ============================================================

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Russian
        ("один час", "01:00"),
        ("два часа", "02:00"),
        ("три часа", "03:00"),
        ("четыре часа", "04:00"),
        ("пять часов", "05:00"),
        ("шесть часов", "06:00"),
        ("семь часов", "07:00"),
        ("восемь часов", "08:00"),
        ("девять часов", "09:00"),
        ("двенадцать часов", "12:00"),

        # English
        ("one hour", "01:00"),
        ("two hours", "02:00"),
        ("three hours", "03:00"),
        ("four hours", "04:00"),
        ("five hours", "05:00"),
        ("six hours", "06:00"),
        ("seven hours", "07:00"),
        ("eight hours", "08:00"),
        ("nine hours", "09:00"),
        ("twelve hours", "12:00"),
    ],
)
async def test_clock_time_stage_3(
    text: str,
    expected: str,
):
    await check_time(text, expected)


# ============================================================
# STAGE 4
# y minutes
# ============================================================

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Russian
        ("одна минута", "00:01"),
        ("две минуты", "00:02"),
        ("три минуты", "00:03"),
        ("пять минут", "00:05"),
        ("десять минут", "00:10"),
        ("пятнадцать минут", "00:15"),
        ("двадцать минут", "00:20"),
        ("двадцать пять минут", "00:25"),
        ("тридцать минут", "00:30"),
        ("пятьдесят девять минут", "00:59"),

        # English
        ("one minute", "00:01"),
        ("two minutes", "00:02"),
        ("three minutes", "00:03"),
        ("five minutes", "00:05"),
        ("ten minutes", "00:10"),
        ("fifteen minutes", "00:15"),
        ("twenty minutes", "00:20"),
        ("twenty five minutes", "00:25"),
        ("thirty minutes", "00:30"),
        ("fifty nine minutes", "00:59"),
    ],
)
async def test_clock_time_stage_4(
    text: str,
    expected: str,
):
    await check_time(text, expected)


# ============================================================
# STAGE 5
# x
# Plain number = hour
# ============================================================

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Russian
        ("один", "01:00"),
        ("два", "02:00"),
        ("три", "03:00"),
        ("четыре", "04:00"),
        ("пять", "05:00"),
        ("шесть", "06:00"),
        ("семь", "07:00"),
        ("девять", "09:00"),
        ("двенадцать", "12:00"),
        ("двадцать три", "23:00"),

        # English
        ("one", "01:00"),
        ("two", "02:00"),
        ("three", "03:00"),
        ("four", "04:00"),
        ("five", "05:00"),
        ("six", "06:00"),
        ("seven", "07:00"),
        ("nine", "09:00"),
        ("twelve", "12:00"),
        ("twenty three", "23:00"),
    ],
)
async def test_clock_time_stage_5(
    text: str,
    expected: str,
):
    await check_time(text, expected)