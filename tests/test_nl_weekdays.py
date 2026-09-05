from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_week_day import (
    NLWeekDay,
    Weekday,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, expected",
    [
        ("понедельник", Weekday.MONDAY),
        ("вторник", Weekday.TUESDAY),
        ("среда", Weekday.WEDNESDAY),
        ("четверг", Weekday.THURSDAY),
        ("пятница", Weekday.FRIDAY),
        ("суббота", Weekday.SATURDAY),
        ("воскресенье", Weekday.SUNDAY),
        ("по выходным", (Weekday.SATURDAY, Weekday.SUNDAY)),
        (
            "по будням",
            (
                Weekday.MONDAY,
                Weekday.TUESDAY,
                Weekday.WEDNESDAY,
                Weekday.THURSDAY,
                Weekday.FRIDAY,
            ),
        ),
    ],
)
async def test_weekday_value_only(text, expected):
    res = await pattern_parser.parse_object(NLWeekDay, text)

    assert res.obj.value == expected