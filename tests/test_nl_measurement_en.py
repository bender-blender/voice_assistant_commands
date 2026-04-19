import pytest

import pint

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_measurement.specific_quantities import (
    NLMeasurementMinute,
    NLMeasurementKilogram,
    NLMeasurementCelsius
)


unit = pint.UnitRegistry()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "class_type,text",
    [
        (NLMeasurementKilogram, "buy ten kilograms of apples"),
        (NLMeasurementMinute, "Order pizza in twenty-two minutes"),
        (NLMeasurementCelsius, "temperature forty-five degrees celsius"),
    ],
)
async def test_groups_parse(class_type, text):
    result = await pattern_parser.parse_object(class_type,text)
    assert result.obj.value is not None