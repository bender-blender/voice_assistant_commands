from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern
from stark.core.types import Object


from voice_commands.nl_types.parsing_context import pattern_parser


class NLLocation(Object):
    
    value: str
    @classproperty
    def pattern(self) -> Pattern:
        return Pattern("**")


        
pattern_parser.register_parameter_type(
    NLLocation)