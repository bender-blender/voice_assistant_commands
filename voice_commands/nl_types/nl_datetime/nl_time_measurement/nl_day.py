from datetime import datetime

from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString
from stark.core.parsing import Pattern,ParseError
from stark.core.types import Object


from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber

class NLDay(Object):
    
    value: float
    day: NLNumber
    
    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("(on the )?$day:NLNumber( числ*)?")

    async def did_parse(self, from_string: LocaleString) -> str:
        if self.day.is_ordinal is False:
            raise ParseError("day not found")

        self.value = self.day.value
        return from_string

pattern_parser.register_parameter_type(NLDay) 