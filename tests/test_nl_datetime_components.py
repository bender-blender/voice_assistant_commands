import pytest

from stark.core.parsing import ParseError

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.reusable_types.nl_datatime_components import (
    NLDateComponents,
)
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_week_day import (
    Weekday,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("первое января", "01.01.2026"),
        ("второе сентября", "02.09.2026"),
        ("пятое октября", "05.10.2026"),
        ("десятое ноября", "10.11.2026"),
        ("двадцать первое декабря", "21.12.2026"),
        ("тридцать первое декабря", "31.12.2026"),
    ],
)
async def test_date_components_calendar_date(text, expected):
    result = await pattern_parser.parse_object(
        NLDateComponents,
        text,
    )

    assert result.obj.calendar_date is not None
    assert result.obj.calendar_date.value == expected
    assert str(result.substring) == text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("понедельник", Weekday.MONDAY),
        ("в понедельник", Weekday.MONDAY),

        ("вторник", Weekday.TUESDAY),
        ("во вторник", Weekday.TUESDAY),

        ("среду", Weekday.WEDNESDAY),
        ("в среду", Weekday.WEDNESDAY),

        ("четверг", Weekday.THURSDAY),
        ("в четверг", Weekday.THURSDAY),

        ("пятницу", Weekday.FRIDAY),
        ("в пятницу", Weekday.FRIDAY),

        ("субботу", Weekday.SATURDAY),
        ("в субботу", Weekday.SATURDAY),

        ("воскресенье", Weekday.SUNDAY),
        ("в воскресенье", Weekday.SUNDAY),
    ],
)
async def test_date_components_weekday(text, expected):
    result = await pattern_parser.parse_object(
        NLDateComponents,
        text,
    )

    assert result.obj.weekday is not None
    assert result.obj.weekday.value == expected
    assert str(result.substring) == text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Неоднозначное время 1-12
        ("в час", ("01:00", "13:00")),
        ("в два", ("02:00", "14:00")),
        ("в три", ("03:00", "15:00")),
        ("в пять", ("05:00", "17:00")),
        ("в семь", ("07:00", "19:00")),
        ("в десять", ("10:00", "22:00")),
        ("в одиннадцать", ("11:00", "23:00")),
        ("в двенадцать", ("12:00", "24:00")),

        # Однозначное время
        ("в тринадцать", "13:00"),
        ("в четырнадцать", "14:00"),
        ("в пятнадцать", "15:00"),
        ("в восемнадцать", "18:00"),
        ("в двадцать", "20:00"),
        ("в двадцать два", "22:00"),
        ("в двадцать три", "23:00"),

        # С единицей измерения
        ("в один час", ("01:00", "13:00")),
        ("в пять часов", ("05:00", "17:00")),
        ("в одиннадцать часов", ("11:00", "23:00")),
        ("в тринадцать часов", "13:00"),
        ("в двадцать два часа", "22:00"),
    ],
)
async def test_date_components_clock(text, expected):
    result = await pattern_parser.parse_object(
        NLDateComponents,
        text,
    )

    assert result.obj.clock is not None
    assert result.obj.clock.value == expected
    assert str(result.substring) == text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("в час пятнадцать", ("01:15", "13:15")),
        ("в два тридцать", ("02:30", "14:30")),
        ("в пять сорок пять", ("05:45", "17:45")),
        ("в одиннадцать пятьдесят", ("11:50", "23:50")),

        ("в тринадцать пятнадцать", "13:15"),
        ("в пятнадцать тридцать", "15:30"),
        ("в восемнадцать сорок пять", "18:45"),
        ("в двадцать два тридцать", "22:30"),
    ],
)
async def test_date_components_clock_with_minutes(text, expected):
    result = await pattern_parser.parse_object(
        NLDateComponents,
        text,
    )

    assert result.obj.clock is not None
    assert result.obj.clock.value == expected
    assert str(result.substring) == text


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     ("text", "weekday", "clock"),
#     [
#         (
#             "в понедельник в час",
#             Weekday.MONDAY,
#             ("01:00", "13:00"),
#         ),
#         (
#             "во вторник в тринадцать",
#             Weekday.TUESDAY,
#             "13:00",
#         ),
#         (
#             "в среду в пять",
#             Weekday.WEDNESDAY,
#             ("05:00", "17:00"),
#         ),
#         (
#             "в четверг в восемнадцать",
#             Weekday.THURSDAY,
#             "18:00",
#         ),
#         (
#             "в пятницу в одиннадцать",
#             Weekday.FRIDAY,
#             ("11:00", "23:00"),
#         ),
#         (
#             "в субботу в двадцать",
#             Weekday.SATURDAY,
#             "20:00",
#         ),
#         (
#             "в воскресенье в двадцать три",
#             Weekday.SUNDAY,
#             "23:00",
#         ),
#     ],
# )
# async def test_date_components_weekday_and_clock(
#     text,
#     weekday,
#     clock,
# ):
#     result = await pattern_parser.parse_object(
#         NLDateComponents,
#         text,
#     )

#     assert result.obj.weekday is not None
#     assert result.obj.weekday.value == weekday

#     assert result.obj.clock is not None
#     assert result.obj.clock.value == clock

#     assert str(result.substring) == text


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     ("text", "date", "clock"),
#     [
#         (
#             "второе сентября в час",
#             "02.09.2026",
#             ("01:00", "13:00"),
#         ),
#         (
#             "пятое октября в пять",
#             "05.10.2026",
#             ("05:00", "17:00"),
#         ),
#         (
#             "десятое ноября в тринадцать",
#             "10.11.2026",
#             "13:00",
#         ),
#         (
#             "двадцать первое декабря в двадцать два",
#             "21.12.2026",
#             "22:00",
#         ),
#     ],
# )
# async def test_date_components_calendar_date_and_clock(
#     text,
#     date,
#     clock,
# ):
#     result = await pattern_parser.parse_object(
#         NLDateComponents,
#         text,
#     )

#     assert result.obj.calendar_date is not None
#     assert result.obj.calendar_date.value == date

#     assert result.obj.clock is not None
#     assert result.obj.clock.value == clock

#     assert str(result.substring) == text