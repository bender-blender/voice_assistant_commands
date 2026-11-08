from dateparser import parse

from stark.core.parsing import Pattern,ParseError
from stark.core.types import NLObject
from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString

from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_type_time import (
    NLMeasurementHour,
    NLMeasurementMinute,
)


class NLClockTime(NLObject):
    value: str | tuple[str, str]

    hour_measurement: NLMeasurementHour | None = None

    minute_measurement: NLMeasurementMinute | None = None
    minute_number_after_measurement: NLNumber | None = None

    minute_only: NLMeasurementMinute | None = None

    hour_number: NLNumber | None = None
    minute_number: NLNumber | None = None

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(
            "(в |in )?("
            "$hour_measurement:NLMeasurementHour"
            "("
            " $minute_measurement:NLMeasurementMinute"
            "|"
            " $minute_number_after_measurement:NLNumber"
            ")?"
            "|"
            "$minute_only:NLMeasurementMinute"
            "|"
            "$hour_number:NLNumber"
            "( $minute_number:NLNumber)?"
            ")"
        )

    def format_time(self, hour, minute) -> str:
        return f"{int(hour):02d}:{int(minute):02d}"

    def get_daytime_and_nighttime(self, hour: int) -> tuple[int,int] | int:
        if hour <= 12:
            return hour, hour + 12

        return hour
    
    def check_clock(self,hour:int,minute:int):
        if 0 < hour <= 24 and 0 <= minute <= 59:
            return True
        return False
    
    async def did_parse(self,from_string: LocaleString) -> str:
        hour = 0
        minute = 0

        if self.hour_measurement is not None:
            hour = self.hour_measurement.number.value

            if self.minute_measurement is not None:
                minute = self.minute_measurement.number.value
            
            elif self.minute_number_after_measurement is not None:
                minute = self.minute_number_after_measurement.value

        elif self.minute_only is not None:
            minute = self.minute_only.number.value

        elif self.hour_number is not None:
            hour = self.hour_number.value

            if self.minute_number is not None:
                minute = self.minute_number.value

        if not self.check_clock(hour,minute):
            raise ParseError("Invalid data")

        hours = self.get_daytime_and_nighttime(hour)
        
        if isinstance(hours,int):
            self.value = (self.format_time(hours,minute))
            return from_string

        self.value = (self.format_time(hours[0],minute),self.format_time(hours[1],minute))
        return from_string

    def resolve(self):
        if isinstance(self.value,str):
            return parse(self.value)

        if isinstance(self.value,tuple):
            dates = [parse(date).strftime("%d.%m.%Y %H:%M:%S") for date in self.value]
            return dates
        
        return None

pattern_parser.register_parameter_type(NLClockTime)