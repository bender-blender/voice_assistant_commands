from stark.core.parsing import PatternParser, ObjectParser, Pattern
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
    


class NLNumberParse(ObjectParser):
    def __init__(self, pattern_parser: PatternParser):
        self.pattern_parser = pattern_parser

    async def did_parse(self, obj:NLNumber, from_string: str) -> str:
        delegate = NLNumberDelegate().parse(from_string)
        obj.value = round(delegate[0],2) #type: ignore
        obj.is_ordinal = delegate[1] #type: ignore
        return from_string


pattern_parser.register_parameter_type(
    NLNumber, parser=NLNumberParse(pattern_parser))
