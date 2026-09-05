import pytest

from datetime import datetime,timedelta
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_relative_day import NLRelativeDay
from voice_commands.nl_types.parsing_context import pattern_parser

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "delta"),
    [
        ("сегодня", 0),
        ("вчера", -1),
        ("позавчера", -2),
        ("позапозавчера", -3),
        ("завтра", 1),
        ("послезавтра", 2),
        ("послепослезавтра", 3),
    ],
)
async def test_relative_day(text, delta):
    result = await pattern_parser.parse_object(NLRelativeDay,text)

    expected = (datetime.now() + timedelta(days=delta)).date()
    assert result.substring == text
    assert result.obj.value.date() == expected