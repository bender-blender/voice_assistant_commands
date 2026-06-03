from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_now import NLNow
from voice_commands.nl_types.parsing_context import pattern_parser
from datetime import datetime
import pytest


@pytest.mark.parametrize(
    "text,value,substring",
    [
        ("Прямо сейчас",datetime.now(),"сейчас"),
        ("Right now",datetime.now(),"now")
    ]
)
@pytest.mark.asyncio
async def test_nl_now(text,value,substring):
    parse = await pattern_parser.parse_object(NLNow,text)
    date = parse.obj.value
    assert parse.substring == substring
    assert (date.year,date.month,date.day,date.hour,date.minute) \
    == (value.year,value.month,value.day,value.hour,value.minute)