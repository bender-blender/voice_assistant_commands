from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern
from stark.core.parsing import NLObject


from voice_commands.nl_types.parsing_context import pattern_parser

from datetime import datetime, timedelta
from enum import IntEnum

from typing import Literal

class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6



class NLMonday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("понедельник*")
    

class NLTuesday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("вторник*")
    

class NLWednesday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("сред*")
    


class NLThursday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("четверг*")
    


class NLFriday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("пятниц*")
    

class NLSaturday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("суббот*")

class NLSunday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("воскресень*")



class NLWorkdays(NLObject):
    value:bool = True
    schedule = (Weekday.MONDAY,Weekday.TUESDAY,Weekday.WEDNESDAY,Weekday.THURSDAY,Weekday.FRIDAY)
    
    @classproperty
    def pattern(cls):
        return Pattern("(по )?(будн*|рабочим)")
    
    def reset_days(self,value:tuple):
        self.schedule = value



class NLWeekend(NLObject):
    value:bool = True
    schedule = (Weekday.SATURDAY,Weekday.SUNDAY)

    @classproperty
    def pattern(cls):
        return Pattern("(по|на )?выходн*")
    
    def reset_days(self,value:tuple):
        self.schedule = value


class NLWeekDay(NLObject):
    value: Weekday | tuple | None = None

    monday:NLMonday | None = None
    tuesday:NLTuesday | None = None
    wednesday:NLWednesday | None = None
    thursday:NLThursday | None = None
    friday:NLFriday | None = None
    saturday:NLSaturday | None = None
    sunday:NLSunday | None = None
    
    weekend: NLWeekend | None = None
    workdays: NLWorkdays | None = None


    @classproperty
    def pattern(cls):
        return Pattern("($weekend:NLWeekend|$workdays:NLWorkdays|$monday:NLMonday|$tuesday:NLTuesday|$wednesday:NLWednesday|$thursday:NLThursday|$friday:NLFriday|$saturday:NLSaturday|$sunday:NLSunday)")
    

    async def did_parse(self, from_string):
        if self.monday:
            self.value = Weekday.MONDAY
        elif self.tuesday:
            self.value = Weekday.TUESDAY
        elif self.wednesday:
            self.value = Weekday.WEDNESDAY
        elif self.thursday:
            self.value = Weekday.THURSDAY
        elif self.friday:
            self.value = Weekday.FRIDAY
        elif self.saturday:
            self.value = Weekday.SATURDAY
        elif self.sunday:
            self.value = Weekday.SUNDAY
        elif self.workdays:
            self.value = self.workdays.schedule
        elif self.weekend:
            self.value = self.weekend.schedule
        return from_string
    

    def resolve(self,value: Weekday | tuple[Weekday],mode: Literal["Last", "This", "Next"] = "This"):
        today = datetime.today()

        if isinstance(value, Weekday):
            value = (value,)


        if mode == "Last":
            dates = [(today + timedelta(days=((day - today.weekday()) - 7))).date() for day in value]

        if mode == "Next":
            dates = [(today + timedelta(days=((day - today.weekday()) + 7))).date() for day in value]

        if mode == "This":
            dates = [(today + timedelta(days=((day - today.weekday()) % 7))).date() for day in value]
        
        return dates


pattern_parser.register_parameter_type(NLWeekend)
pattern_parser.register_parameter_type(NLWorkdays)
pattern_parser.register_parameter_type(NLMonday)
pattern_parser.register_parameter_type(NLTuesday)
pattern_parser.register_parameter_type(NLWednesday)
pattern_parser.register_parameter_type(NLThursday)
pattern_parser.register_parameter_type(NLFriday)
pattern_parser.register_parameter_type(NLSaturday)
pattern_parser.register_parameter_type(NLSunday)
pattern_parser.register_parameter_type(NLWeekDay)