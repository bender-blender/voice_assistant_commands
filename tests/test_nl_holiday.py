import pytest

from datetime import datetime

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_holiday import NLHoliday


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected_start", "expected_end", "sub"),
    [
        (
            "еженедельная перезагрузка",
            datetime(2026, 8, 30, 11, 0),
            datetime(2026, 8, 30, 12, 0),
            "еженедельная перезагрузка",
        ),
    ],
)
async def test_nl_holiday(
    text,
    expected_start,
    expected_end,
    sub,
):
    result = await pattern_parser.parse_object(
        NLHoliday,
        text,
    )

    start, end = result.obj.resolve()

    assert start == expected_start
    assert end == expected_end
    assert str(result.substring) == sub