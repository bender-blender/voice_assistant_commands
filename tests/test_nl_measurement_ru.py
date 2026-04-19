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
    "class_type,text,sub,value",
    [
        (NLMeasurementKilogram, "купи десять килограмм яблок","десять килограмм",10 * unit.kilogram),
        (NLMeasurementMinute, "через двадцать две минуты закажи пиццу", "двадцать две минуты", 22 * unit.minute),
        (NLMeasurementCelsius, "температура сорок пять градусов цельсия", "сорок пять градусов цельсия", unit.Quantity(45, unit.degree_Celsius)),
    ],
)
async def test_groups_parse(class_type, text, sub, value):
    result = await pattern_parser.parse_object(class_type,text)
    assert result.substring == sub
    assert result.obj.value == value 