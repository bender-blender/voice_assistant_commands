from datetime import datetime, timedelta

import pytest

from voice_commands.parameters.date_time import DateTime


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query, expected_substr, expected_offset_days",
    [
        ("погода в городе киев завтра", "завтра", 1),
        ("погода послезавтра в москве", "послезавтра", 2),
        ("какая погода сегодня в харькове", "сегодня", 0),
    ],
)
async def test_datetime(query, expected_substr, expected_offset_days):
    parameter = DateTime(value=None)
    substr = await parameter.did_parse(query)

    assert isinstance(substr, str)
    assert substr in query
    assert expected_substr in substr

    expected_date = datetime.now() + timedelta(days=expected_offset_days)
    assert abs(parameter.value - expected_date) < timedelta(minutes=1)
