from stark.core.parsing import PatternParser, ObjectParser,Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object


from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_type_time import (
    NLMeasurementSecond,
    NLMeasurementMinute,
    NLMeasurementHour,
    NLMeasurementDay,
    NLMeasurementWeek,
    NLMeasurementMonth,
    NLMeasurementYear
)
from voice_commands.nl_types.parsing_context import pattern_parser


class NLTimeMeasurement(Object):
 
    value:float
    primitives = [
        NLMeasurementDay,NLMeasurementHour,NLMeasurementMinute,NLMeasurementMonth,
        NLMeasurementSecond,NLMeasurementWeek,NLMeasurementYear]
    
    async def did_parse(self, from_string):
        
        for primitive in self.primitives:
            try:
                parse = await pattern_parser.parse_object(primitive,from_string)
                if parse:
                    self.value = parse.obj.value
                    return parse.substring
            except ParseError:
                continue
        raise ParseError("value not found")
    
pattern_parser.register_parameter_type(NLTimeMeasurement)