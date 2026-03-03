from .duration_interval import DurationInterval, DurationIntervalParse
from voice_commands.nl_types.parsing_context import pattern_parser


class NLSecond(DurationInterval):
    pass

class NLSecondParse(DurationIntervalParse):
    pass


class NLMinute(DurationInterval):
    pass

class NLMinuteParse(DurationIntervalParse):
    pass


class NLHour(DurationInterval):
    pass

class NLHourParse(DurationIntervalParse):
    pass



class NLDay(DurationInterval):
    pass

class NLDayParse(DurationIntervalParse):
    pass



class NLMonth(DurationInterval):
    pass

class NLMonthParse(DurationIntervalParse):
    pass



class NLYear(DurationInterval):
    pass

class NLYearParse(DurationIntervalParse):
    pass




pattern_parser.register_parameter_type(NLSecond,NLSecondParse(pattern_parser,["сек","second"]))
pattern_parser.register_parameter_type(NLMinute,NLMinuteParse(pattern_parser,["мин","minute"]))
pattern_parser.register_parameter_type(NLHour,NLHourParse(pattern_parser,["час","hour"]))
pattern_parser.register_parameter_type(NLDay,NLDayParse(pattern_parser,["дн","день","day"]))
pattern_parser.register_parameter_type(NLMonth,NLMonthParse(pattern_parser,["месяц","month"]))
pattern_parser.register_parameter_type(NLYear,NLYearParse(pattern_parser,["год","лет","year"]))