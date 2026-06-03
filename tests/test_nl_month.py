
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_month import Month,NLMonth
from voice_commands.nl_types.parsing_context import pattern_parser
import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("январь", Month.JANUARY),
        ("в январе", Month.JANUARY),
        ("15 января", Month.JANUARY),

        ("февраль", Month.FEBRUARY),
        ("в феврале", Month.FEBRUARY),

        ("март", Month.MARCH),
        ("в марте", Month.MARCH),

        ("апрель", Month.APRIL),
        ("в апреле", Month.APRIL),

        ("май", Month.MAY),
        ("в мае", Month.MAY),

        ("июнь", Month.JUNE),
        ("в июне", Month.JUNE),

        ("июль", Month.JULY),
        ("в июле", Month.JULY),

        ("август", Month.AUGUST),
        ("в августе", Month.AUGUST),

        ("сентябрь", Month.SEPTEMBER),
        ("в сентябре", Month.SEPTEMBER),

        ("октябрь", Month.OCTOBER),
        ("в октябре", Month.OCTOBER),

        ("ноябрь", Month.NOVEMBER),
        ("в ноябре", Month.NOVEMBER),

        ("декабрь", Month.DECEMBER),
        ("в декабре", Month.DECEMBER),
    ],
)
async def test_did_parse_month(text, expected):
    result = await pattern_parser.parse_object(NLMonth,text)
    assert result.substring in text
    assert result.obj.value == expected

