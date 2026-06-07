from stark.general.classproperty import classproperty
from stark.core.parsing import ParseError
from stark.core.parsing import Pattern
from stark.core.parsing import Object


from voice_commands.nl_types.parsing_context import pattern_parser


from enum import auto,IntEnum
from datetime import time


class DayPart(IntEnum):
    morning = auto()
    noon =  auto()
    afternoon =  auto()
    evening = auto()
    night = auto()



class NLDayPart_Morning(Object):

    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("утр*")
    

class NLDayPart_Noon(Object):

    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("полд*")
    
class NLDayPart_Afternoon(Object):

    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("во второй половине дня")
    

class NLDayPart_Evening(Object):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("вечер*")


class NLDayPart_Night(Object):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("ноч*")
    


class NLDayPart(Object):

    value:time
    
    morning: NLDayPart_Morning
    noon: NLDayPart_Noon
    afternoon: NLDayPart_Afternoon
    evening: NLDayPart_Evening
    night: NLDayPart_Night

    @classproperty
    def pattern(cls):
        return Pattern("($morning:NLDayPart_Morning|$noon:NLDayPart_Noon|$afternoon:NLDayPart_Afternoon|$evening:NLDayPart_Evening|$night:NLDayPart_Night)")
    
    async def did_parse(self, from_string):
        data = self.resolve()
        if self.morning:
            self.value = data[DayPart.morning]
        elif self.noon:
            self.value = data[DayPart.noon]
        elif self.afternoon:
            self.value = data[DayPart.afternoon]
        elif self.evening:
            self.value = data[DayPart.evening]
        elif self.night:
            self.value = data[DayPart.night]
        return from_string

    def resolve(self):
        return {DayPart.morning:time(hour=9),
                DayPart.noon:time(hour=12),
                DayPart.afternoon:time(hour=13),
                DayPart.evening:time(hour=17),
                DayPart.night:time(hour=22)
                }
        

pattern_parser.register_parameter_type(NLDayPart_Morning)
pattern_parser.register_parameter_type(NLDayPart_Night)
pattern_parser.register_parameter_type(NLDayPart_Noon)
pattern_parser.register_parameter_type(NLDayPart_Evening)
pattern_parser.register_parameter_type(NLDayPart_Afternoon)
pattern_parser.register_parameter_type(NLDayPart)