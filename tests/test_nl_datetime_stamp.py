import pytest

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_datetime.top_level_composite_types.nl_datetime_stamp import (
    NLDatetimeStamp,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected_substring"),
    [
        ("второе сентября", "второе сентября"),
        ("в пятницу", "в пятницу"),
        ("в час", "в час"),
        ("в одиннадцать", "в одиннадцать"),
        ("в тринадцать", "в тринадцать"),
        ("в час пятнадцать", "в час пятнадцать"),
        ("в пятницу в час", "в пятницу в час"),
        ("второе сентября в тринадцать", "второе сентября в тринадцать"),
    ],
)
async def test_datetime_stamp_parse(
    text,
    expected_substring,
):
    result = await pattern_parser.parse_object(
        NLDatetimeStamp,
        text,
    )

    assert result.obj.component is not None
    assert result.obj.value is not None
    assert str(result.substring) == expected_substring


#! For resolve
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "второе сентября",
        "в пятницу",
        "в час",
        "в одиннадцать",
        "в тринадцать",
        "в час пятнадцать",
        "в пятницу в час",
        "второе сентября в тринадцать",
    ],
)
async def test_datetime_stamp_resolve(text):
    result = await pattern_parser.parse_object(
        NLDatetimeStamp,
        text,
    )

    resolved = result.obj.resolve()

    assert resolved is not None



#! For modes
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "mode"),
    [
        ("в пятницу", "Last"),
        ("в пятницу", "This"),
        ("в пятницу", "Next"),

        ("в пятницу в час", "Last"),
        ("в пятницу в час", "This"),
        ("в пятницу в час", "Next"),
    ],
)
async def test_datetime_stamp_modes(
    text,
    mode,
):
    result = await pattern_parser.parse_object(
        NLDatetimeStamp,
        text,
    )

    resolved = result.obj.resolve(mode)

    assert resolved is not None