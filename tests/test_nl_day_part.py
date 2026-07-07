import pytest
from datetime import time

from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_day_part import (
    NLDayPartUnion
)

from voice_commands.nl_types.parsing_context import pattern_parser


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected", "sub"),
    [
        ("Напомни утром", time(hour=9), "утром"),
        ("Завтра в полдень", time(hour=12), "полдень"),
        ("во второй половине дня", time(hour=13), "во второй половине дня"),
        ("Закажи вечером", time(hour=17), "вечером"),
        ("Выключи ночью", time(hour=22), "ночью"),
    ],
)
async def test_nl_day_part(text, expected, sub):
    union = NLDayPartUnion()
    result = await pattern_parser.parse_object(NLDayPartUnion,text)
    parse_time = union.resolve(result.obj.value.value)
    assert parse_time == expected
    assert str(result.substring) == sub
