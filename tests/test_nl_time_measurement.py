from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_time_measurement import NLTimeMeasurement
from voice_commands.nl_types.parsing_context import pattern_parser
from pint import UnitRegistry
import pytest

unit = UnitRegistry()



@pytest.mark.parametrize(
    "text,value,substring",
    [
        ("через пять лет планирую переезд", 5 * unit.year, "пять лет"),
        ("вернусь через три года", 3 * unit.year, "три года"),
        ("через десять лет это случится", 10 * unit.year, "десять лет"),
        ("подожди семь минут", 7 * unit.minute, "семь минут"),
        ("таймер на пятнадцать минут", 15 * unit.minute, "пятнадцать минут"),
        ("через два часа выходим", 2 * unit.hour, "два часа"),
        ("остался один час", 1 * unit.hour, "один час"),
        ("через тридцать секунд старт", 30 * unit.second, "тридцать секунд"),
        ("отпуск через четыре месяца", 4 * unit.month, "четыре месяца"),
        ("событие через двенадцать дней", 12 * unit.day, "двенадцать дней"),
    ]
)
@pytest.mark.asyncio
async def test_nl_time_measurement(text,value,substring):
    parse = await pattern_parser.parse_object(NLTimeMeasurement,text)
    assert parse.substring == substring
    assert parse.obj.value == value
