from voice_commands.nl_types.nl_measurement.nl_measurement import NLMeasurement,NLAbstractUnit
from voice_commands.nl_types.nl_measurement.generation_pattern import create_pattern
from voice_commands.nl_types.parsing_context import pattern_parser
from pint import UnitRegistry


unit = UnitRegistry()

class NLUnitSecond(NLAbstractUnit):
    _unit_keywords = create_pattern(False,"сек*","second*")
    key = unit.second

class NLMeasurementSecond(NLMeasurement):
    _unit_type = NLUnitSecond



class NLUnitMinute(NLAbstractUnit):
    _unit_keywords = create_pattern(False,"минут*","minute*")
    key = unit.minute

class NLMeasurementMinute(NLMeasurement):
    _unit_type = NLUnitMinute



class NLUnitHour(NLAbstractUnit):
    _unit_keywords = create_pattern(False,"час*","hour*")
    key = unit.hour

class NLMeasurementHour(NLMeasurement):
    _unit_type = NLUnitHour



class NLUnitDay(NLAbstractUnit):
    _unit_keywords = create_pattern(False,"дн*","день","day*")
    key = unit.day

class NLMeasurementDay(NLMeasurement):
    _unit_type = NLUnitDay


class NLUnitWeek(NLAbstractUnit):
    _unit_keywords = create_pattern(False,"недел*","week*")
    key = unit.week

class NLMeasurementWeek(NLMeasurement):
    _unit_type = NLUnitWeek


class NLUnitMonth(NLAbstractUnit):
    _unit_keywords = create_pattern(False,"месяц*","month*")
    key = unit.month

class NLMeasurementMonth(NLMeasurement):
    _unit_type = NLUnitMonth


class NLUnitYear(NLAbstractUnit):
    _unit_keywords = create_pattern(False,"год*","лет","year*")
    key = unit.year

class NLMeasurementYear(NLMeasurement):
    _unit_type = NLUnitYear


def auto_register(module_globals):
    for obj in module_globals.values():
        if isinstance(obj,type) and issubclass(obj, (NLAbstractUnit, NLMeasurement)):
            try:
                pattern_parser.register_parameter_type(obj)
            except Exception:
                pass

auto_register(globals())