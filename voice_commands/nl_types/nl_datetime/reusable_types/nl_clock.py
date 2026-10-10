from dateparser import parse

from stark.core.parsing import Pattern,ParseError
from stark.core.types import Object
from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_type_time import (
    NLMeasurementHour,
    NLMeasurementMinute,
)


class NLClokTime(Object):
    value: str

    hour_measurement: NLMeasurementHour | None = None
    minute_measurement: NLMeasurementMinute | None = None

    minute_only: NLMeasurementMinute | None = None

    hour_number: NLNumber | None = None
    minute_number: NLNumber | None = None

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(
            "("
            "$hour_measurement:NLMeasurementHour"
            "( $minute_measurement:NLMeasurementMinute)?"
            "|"
            "$minute_only:NLMeasurementMinute"
            "|"
            "$hour_number:NLNumber"
            "( $minute_number:NLNumber)?"
            ")"
        )

    def format_time(self, hour, minute) -> str:
        return f"{int(hour):02d}:{int(minute):02d}"

    def check_clock(self,hour:int,minute:int):
        if 0 < hour < 23 and 0 < minute <= 59:
            return True
        return False
    
    async def did_parse(self,from_string: LocaleString) -> str:
        hour = 0
        minute = 0

        if self.hour_measurement is not None:
            hour = self.hour_measurement.number.value

            if self.minute_measurement is not None:
                minute = self.minute_measurement.number.value

        elif self.minute_only is not None:
            minute = self.minute_only.number.value

        elif self.hour_number is not None:
            hour = self.hour_number.value

            if self.minute_number is not None:
                minute = self.minute_number.value

        if not self.check_clock(hour,minute):
            raise ValueError("Invalid data")
        
        self.value = self.format_time(
            hour,
            minute,
        )

        return from_string

    def resolve(self):
        return parse(self.value)


pattern_parser.register_parameter_type(NLClokTime)