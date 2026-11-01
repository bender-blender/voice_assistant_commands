from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern
from stark.core.parsing import NLObject


from voice_commands.nl_types.parsing_context import pattern_parser

from datetime import datetime,timedelta
from enum import auto,IntEnum


class RelativeDay(IntEnum):
    today = auto()
    tomorrow = auto()
    yesterday = auto()
    day_before_yesterday = auto()
    day_after_tomorrow = auto()
    two_before = auto()
    two_after = auto()



class NLToday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("сегодня")


class NLTomorrow(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("завтра")
    

class NLYesterday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("вчера")
    


class NLDayBeforeYesterday(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("позавчера")


class NLTwoBefore(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("позапозавчера")
     

class NLDayAfterTomorrow(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("послезавтра")


class NLTwoAfter(NLObject):
    value:bool = True

    @classproperty
    def pattern(cls):
        return Pattern("послепослезавтра")




class NLRelativeDay(NLObject):
    value: str

    today: NLToday
    yesterday: NLYesterday
    tomorrow: NLTomorrow
    day_before_yesterday: NLDayBeforeYesterday
    two_before: NLTwoBefore
    day_after_tomorrow: NLDayAfterTomorrow
    two_after: NLTwoAfter

    @classproperty
    def pattern(cls):
        return Pattern("($today:NLToday|$yesterday:NLYesterday|$tomorrow:NLTomorrow|$day_before_yesterday:NLDayBeforeYesterday|$two_before:NLTwoBefore|$day_after_tomorrow:NLDayAfterTomorrow|$two_after:NLTwoAfter)")
    

    async def did_parse(self, from_string):
        date = self.resolve_calendar_date()
        
        if self.today:
            self.value = date[RelativeDay.today]
        elif self.yesterday:
            self.value = date[RelativeDay.yesterday]
        elif self.tomorrow:
            self.value = date[RelativeDay.tomorrow]
        elif self.day_before_yesterday:
            self.value = date[RelativeDay.day_before_yesterday]
        elif self.two_before:
            self.value = date[RelativeDay.two_before]
        elif self.day_after_tomorrow:
            self.value = date[RelativeDay.day_after_tomorrow]
        elif self.two_after:
            self.value = date[RelativeDay.two_after]
        
        return from_string


    def resolve_calendar_date(self):
        now = datetime.now()

        return {
            RelativeDay.today: now.strftime("%Y-%d-%m"),
            RelativeDay.yesterday: (now - timedelta(days=1)).strftime("%Y-%d-%m"),
            RelativeDay.day_before_yesterday: (now - timedelta(days=2)).strftime("%Y-%d-%m"),
            RelativeDay.tomorrow: (now + timedelta(days=1)).strftime("%Y-%d-%m"),
            RelativeDay.day_after_tomorrow: (now + timedelta(days=2)).strftime("%Y-%d-%m"),
            RelativeDay.two_after: (now + timedelta(days=3)).strftime("%Y-%d-%m"),
            RelativeDay.two_before: (now - timedelta(days=3)).strftime("%Y-%d-%m"),
        }
    

pattern_parser.register_parameter_type(NLTwoBefore)
pattern_parser.register_parameter_type(NLTwoAfter)
pattern_parser.register_parameter_type(NLDayAfterTomorrow)
pattern_parser.register_parameter_type(NLDayBeforeYesterday)
pattern_parser.register_parameter_type(NLToday)
pattern_parser.register_parameter_type(NLYesterday)
pattern_parser.register_parameter_type(NLTomorrow)
pattern_parser.register_parameter_type(NLRelativeDay)