from voice_commands.nl_types.nl_measurement.nl_measurement import NLMeasurement,NLMeasurementParse
from voice_commands.nl_types.parsing_context import pattern_parser
from pint import UnitRegistry
import pytest

unit = UnitRegistry()


@pytest.mark.parametrize('lang, text, expected_magnitude, expected_unit', [
    # English
    ("en", "three point five meters", 3.5, unit.meter),
    ("en", "two kilograms", 2, unit.kilogram),
    ("en", "half liter", 0.5, unit.liter),
    ("en", "minus one hundred grams", -100, unit.gram),

    # Russian
    ("ru", "три целых пять десятых метра", 3.5, unit.meter),
    ("ru", "два килограмма", 2, unit.kilogram),
    ("ru", "поллитра", 0.5, unit.liter),
    ("ru", "минус сто грамм", -100, unit.gram),

    # TODO: test extraction
])
@pytest.mark.asyncio
async def test_nlmeasurement_parse(lang, text, expected_magnitude, expected_unit):
    parsed = await pattern_parser.parse_object(NLMeasurement, text)
    nl_measurement = parsed.obj
    assert nl_measurement.value == expected_magnitude * expected_unit
    
