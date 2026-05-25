from stark.core.parsing import PatternParser, ObjectParser, Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object

from voice_commands.nl_types.nl_number.nl_number_delegate import NLNumberDelegate
from voice_commands.nl_types.parsing_context import pattern_parser


class NLNumber(Object):
    
    value: float
    is_ordinal: bool

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")
    
    async def did_parse(self, from_string: str) -> str:
        delegate = NLNumberDelegate().parse(from_string)

        if delegate is not None:
            self.value = round(delegate[0].value,2)
            self.is_ordinal = delegate[0].ordinal 
            return delegate[1]
        raise ParseError("value not found")
    
    

pattern_parser.register_parameter_type(NLNumber)