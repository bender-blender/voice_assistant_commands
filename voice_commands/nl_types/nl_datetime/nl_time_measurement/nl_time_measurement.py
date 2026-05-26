from stark.core.parsing import PatternParser, ObjectParser,Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object


from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_type_time import (
    NLDay,
    NLHour,
    NLMinute,
    NLMonth,
    NLSecond,
    NLYear,
    DurationInterval,
)
from voice_commands.nl_types.parsing_context import pattern_parser


class NLTimeMeasurement(Object):

    value: float

    @classproperty
    def pattern(cls):
        return Pattern("**")
    


class NLTimeMeasurementParse(ObjectParser):

    def __init__(self, pattern_parse:PatternParser):
        self.pattern_parse = pattern_parse 
        self.primitives:list[type[DurationInterval]] = [
            NLDay,
            NLHour,
            NLMinute,
            NLMonth,
            NLSecond,
            NLYear
        ]
    
    async def did_parse(self, obj:NLTimeMeasurement, from_string):
        
        for primitive in self.primitives:
            try:
                parse = await self.pattern_parse.parse_object(primitive,from_string)
                if parse:
                    obj.value = parse.obj.value
                    return parse.substring
            except ParseError:
                continue
        raise ParseError("value not found")
    

pattern_parser.register_parameter_type(NLTimeMeasurement,NLTimeMeasurementParse(pattern_parser))

