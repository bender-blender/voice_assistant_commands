import pytest

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.additional.time_type import (
    NLPastTimeType,
    NLPresentTimeType,
    NLFutureTimeType,
    NLTimeType,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Present
        ("этот", 0),
        ("эта", 0),
        ("это", 0),
        ("эту", 0),
        ("этой", 0),
        ("текущий", 0),
        ("текущая", 0),
        ("текущую", 0),

        # Past
        ("прошлый", -1),
        ("прошлая", -1),
        ("прошлую", -1),
        ("предыдущий", -1),
        ("предыдущая", -1),
        ("предыдущую", -1),

        # Future
        ("следующий", 1),
        ("следующая", 1),
        ("следующую", 1),
        ("следующей", 1),
        ("будущий", 1),
        ("будущая", 1),
        ("будущую", 1),
    ],
)
async def test_nl_time_type(text, expected):
    result = await pattern_parser.parse_object(
        NLTimeType,
        text,
    )

    assert result.obj.value.value == expected
    assert str(result.substring) == text




@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("parser_type", "text", "expected"),
    [
        (NLPresentTimeType, "этот", 0),
        (NLPresentTimeType, "текущая", 0),

        (NLPastTimeType, "прошлый", -1),
        (NLPastTimeType, "предыдущую", -1),

        (NLFutureTimeType, "следующий", 1),
        (NLFutureTimeType, "будущая", 1),
    ],
)
async def test_time_type_classes(
    parser_type,
    text,
    expected,
):
    result = await pattern_parser.parse_object(
        parser_type,
        text,
    )

    assert result.obj.value == expected
    assert str(result.substring) == text



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "этот месяц",
        "эту неделю",
        "прошлый месяц",
        "прошлую неделю",
        "следующий месяц",
        "следующую неделю",
        "следующую пятницу",
    ],
)
async def test_time_type_in_phrase(text):
    result = await pattern_parser.parse_object(
        NLTimeType,
        text,
    )

    print(text)
    print(result)