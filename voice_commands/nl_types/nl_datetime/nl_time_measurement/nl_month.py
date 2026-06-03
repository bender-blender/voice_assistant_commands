from voice_commands.nl_types.parsing_context import pattern_parser
from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern, ParseError
from stark.core.types import Object
from dateparser import parse
from enum import IntEnum


class Month(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12




class NLMonth(Object):
    value: Month
    data_dict = {
        "январ": Month.JANUARY,
        "феврал": Month.FEBRUARY,
        "март": Month.MARCH,
        "апрел": Month.APRIL,
        "май": Month.MAY,
        "мае": Month.MAY,
        "июн": Month.JUNE,
        "июл": Month.JULY,
        "август": Month.AUGUST,
        "сентябр": Month.SEPTEMBER,
        "октябр": Month.OCTOBER,
        "ноябр": Month.NOVEMBER,
        "декабр": Month.DECEMBER,
    }

    @classproperty
    def pattern(cls):
        return Pattern("(в )?(январ*|феврал*|март*|апрел*|май*|мае|июн*|июл*|август*|сентябр*|октябр*|ноябр*|декабр*)")
    
    async def did_parse(self, from_string):
        for key in self.data_dict:
            if key in from_string:
                self.value = self.data_dict[key]
                return from_string
        raise ParseError("month not found")
    

pattern_parser.register_parameter_type(NLMonth)