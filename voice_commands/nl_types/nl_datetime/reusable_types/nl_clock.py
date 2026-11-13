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

from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_day_part import NLDayPartUnion

from dataclasses import dataclass



@dataclass(frozen=True)
class Clock:
    hour : int
    minute : int
    pm: bool | None


class NLClockTime(NLObject):
    value: Clock

    hour_measurement: NLMeasurementHour | None = None

    minute_measurement: NLMeasurementMinute | None = None
    minute_number_after_measurement: NLNumber | None = None

    minute_only: NLMeasurementMinute | None = None

    hour_number: NLNumber | None = None
    minute_number: NLNumber | None = None

    hour: int
    minute: int
    pm: bool | None = None
    part: NLDayPartUnion

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
            "(( )?$part:NLDayPartUnion)?"
        )

    
    def check_clock(self,hour:int,minute:int):
        if 0 < hour <= 24 and 0 <= minute <= 59:
            return True
        return False
    
    async def did_parse(self,from_string: LocaleString) -> str:
        self.hour = 0
        self.minute = 0

        
        if self.hour_measurement is not None:
            self.hour = self.hour_measurement.number.value
        
            if self.minute_measurement is not None:
                self.minute = self.minute_measurement.number.value
                    
            elif self.minute_number_after_measurement is not None:
                self.minute = self.minute_number_after_measurement.value
        
        elif self.minute_only is not None:
                self.minute = self.minute_only.number.value
        
        elif self.hour_number is not None:
            self.hour = self.hour_number.value
        
            if self.minute_number is not None:
                self.minute = self.minute_number.value
        
        if not self.check_clock(self.hour,self.minute):
            raise ParseError("Invalid data")


        if isinstance(self.part,NLDayPartUnion):
            if self.part.value.value < 2:
                self.pm = True
            else:
                self.pm = False


        self.value = Clock(self.hour,self.minute,self.pm)
        return from_string

    
    def resolve(self):

        if self.pm == True:
            return f"{self.hour:02d}:{self.minute:02d}"

        if self.pm == False:
            return f"{self.hour + 12:02d}:{self.minute:02d}"

        return None

pattern_parser.register_parameter_type(NLClockTime)