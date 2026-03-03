from stark.core.parsing import ObjectParser,PatternParser, Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object


from voice_commands.nl_types.nl_measurement.nl_measurement import NLMeasurement
from voice_commands.nl_types.parsing_context import pattern_parser


class DurationInterval(Object):

    value: float
    
    @classproperty
    def pattern(cls):
        return Pattern("**")
    

class DurationIntervalParse(ObjectParser):

    def __init__(self,pattern_parser:PatternParser, sample:list[str]=[]):
        self.pattern_parser = pattern_parser
        self.sample = sample 

    async def did_parse(self, obj:DurationInterval, from_string):
        if self.sample == []:
            raise ParseError("add a substring pattern to search for")
        
        parse = await pattern_parser.parse_object(NLMeasurement,from_string)
        for sub in self.sample:
            if sub in parse.substring:
                obj.value = parse.obj.value
                return parse.substring

        raise ParseError("value not found")



