from stark.core.parsing import PatternParser, ObjectParser, Pattern
from stark.general.classproperty import classproperty
from stark.core.types import Object


from voice_commands.nl_types.nl_measurement.nl_delegate import MeasurmentDelegate
from voice_commands.nl_types.parsing_context import pattern_parser
from pint import UnitRegistry



class NLUnit(Object):
    value: UnitRegistry

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")


class NLUnitParse(ObjectParser):
    def __init__(self, pattern_parser: PatternParser):
        self.pattern_parser = pattern_parser

    async def did_parse(self,obj:NLUnit, from_string: str) -> str:
        delegate = MeasurmentDelegate().parse(from_string)
        if delegate:
            obj.value = delegate
        return from_string


pattern_parser.register_parameter_type(
    NLUnit, parser=NLUnitParse(pattern_parser))
