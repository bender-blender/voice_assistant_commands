from stark.general.classproperty import classproperty
from stark.core.parsing import Object,Pattern
from stark.core.types import Union

from voice_commands.nl_types.parsing_context import pattern_parser


from enum import IntEnum
from datetime import time


class DayPart(IntEnum):
    morning = 1
    noon =  2
    afternoon = 3
    evening = 4
    night = 5


class ClassParent(Object):


    def resolve(self):
        data = {DayPart.morning:time(hour=9),
                DayPart.noon:time(hour=12),
                DayPart.afternoon:time(hour=13),
                DayPart.evening:time(hour=17),
                DayPart.night:time(hour=22)
                }
        return data[self.value]




class NLDayPart_Morning(ClassParent):
    
    value = 1
    @classproperty
    def pattern(cls):
        return Pattern("утр*")
        

class NLDayPart_Noon(ClassParent):
    
    value = 2
    @classproperty
    def pattern(cls):
        return Pattern("полд*")
    
class NLDayPart_Afternoon(ClassParent):
    
    value = 3
    @classproperty
    def pattern(cls):
        return Pattern("во второй половине дня")
    

class NLDayPart_Evening(ClassParent):
    
    value = 4
    @classproperty
    def pattern(cls):
        return Pattern("вечер*")


class NLDayPart_Night(ClassParent):
    value = 5
    @classproperty
    def pattern(cls):
        return Pattern("ноч*")
    


class NLDayPartUnion(Union):
    _types = [
        NLDayPart_Morning,
        NLDayPart_Night,
        NLDayPart_Noon,
        NLDayPart_Evening,
        NLDayPart_Afternoon,
    ]
    


pattern_parser.register_parameter_type(NLDayPartUnion)