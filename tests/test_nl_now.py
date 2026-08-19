from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_now import NL_Now
from voice_commands.nl_types.parsing_context import pattern_parser

from datetime import datetime

import pytest


@pytest.mark.parametrize(
    "text,substring",
    [
        ("сейчас", "сейчас"),
        ("now", "now"),
        ("что происходит сейчас", "сейчас"),
        ("я сейчас занят", "сейчас"),
        ("давай сделаем это сейчас", "сейчас"),
        ("сейчас я пойду домой", "сейчас"),
        ("кот сейчас спит", "сейчас"),
        ("я хочу знать время сейчас", "сейчас"),
        ("what are you doing now", "now"),
        ("I need it now", "now"),
        ("let's do it now", "now"),
        ("what time is it now", "now"),
    ]
)
@pytest.mark.asyncio
async def test_nl_now(text, substring):
    parse = await pattern_parser.parse_object(NL_Now, text)

    assert parse.substring == substring
    assert isinstance(parse.obj.value, datetime)