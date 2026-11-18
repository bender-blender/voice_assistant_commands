from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString
from stark.core.parsing import Pattern, Union
from stark.core.parsing import NLObject

from voice_commands.nl_types.parsing_context import pattern_parser


class TimeType(NLObject):
    value: int

    present = "(эт*|текущ*)"
    past = "(прошл*|предыдущ*)"
    future = "(следующ*|будущ*)"

    async def did_parse(self, from_string: LocaleString) -> str:
        return from_string

    

class NLPastTimeType(TimeType):
    value = -1

    @classproperty
    def pattern(cls):
        return Pattern(cls.past)


class NLPresentTimeType(TimeType):
    value = 0

    @classproperty
    def pattern(cls):
        return Pattern(cls.present)


class NLFutureTimeType(TimeType):
    value = 1

    @classproperty
    def pattern(cls):
        return Pattern(cls.future)


class NLTimeType(Union):
    _types = [
        NLPastTimeType,
        NLPresentTimeType,
        NLFutureTimeType,
    ]

pattern_parser.register_parameter_type(TimeType)
pattern_parser.register_parameter_type(NLFutureTimeType)
pattern_parser.register_parameter_type(NLPresentTimeType)
pattern_parser.register_parameter_type(NLPastTimeType)
pattern_parser.register_parameter_type(NLTimeType)