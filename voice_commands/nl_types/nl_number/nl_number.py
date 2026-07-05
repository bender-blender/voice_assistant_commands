from stark.core.parsing import Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object

from voice_commands.nl_types.nl_number.nl_number_delegate import NLNumberParser
from voice_commands.nl_types.parsing_context import pattern_parser


class NLNumber(Object):
    
    value: float
    is_ordinal: bool
    negative_signs = ["минус","minus"]
    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")
    


    async def did_parse(self, from_string):
        try:
            parse = NLNumberParser().parse(from_string)
            self.value, self.is_ordinal = parse[0][0],parse[0][1]
            for word in from_string:
                if word in self.negative_signs:
                    self.value, self.is_ordinal = -parse[0][0],parse[0][1]
            return parse[1]
        except TypeError as e:
            if 'cannot unpack non-iterable NoneType object' in str(e): 
                raise ParseError(f"Can't parse a number from {from_string}") from e 
            else:
               raise e
    
pattern_parser.register_parameter_type(NLNumber)