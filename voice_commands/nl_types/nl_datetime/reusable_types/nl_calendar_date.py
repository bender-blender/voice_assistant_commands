from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString
from stark.core.parsing import Pattern,ParseError
from stark.core.types import NLObject



from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_month import NLMonth
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_year import NLYear
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_day import NLDay
from voice_commands.nl_types.parsing_context import pattern_parser

from datetime import datetime
from typing import Literal


class NLCalendarDate(NLObject):
    value: str
    day: NLDay | None = None
    month: NLMonth | None = None
    year: NLYear | None = None

    now = datetime.now()

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$day:NLDay( $month:NLMonth( $year:NLYear)?)?")

    async def did_parse(self, from_string: LocaleString) -> str:

        if self.day is None:
            raise ParseError
        
        if self.month is None:
            self.month = self.now.month

        if self.year is None:
            self.year = self.now.year
    
        self.value = f"{self.day:02d}.{self.month:02d}.{self.year}"
    
        return from_string

    def resolve(self,mode: Literal["Last", "This", "Next"] = "This"):

        if mode == "Last":
            self.year -= 1
        
        elif mode == "Next":
            self.year += 1
        
        self.value = f"{self.day:02d}.{self.month:02d}.{self.year}"
        return datetime.strptime(self.value,"%d.%m.%Y")

       

pattern_parser.register_parameter_type(NLCalendarDate)