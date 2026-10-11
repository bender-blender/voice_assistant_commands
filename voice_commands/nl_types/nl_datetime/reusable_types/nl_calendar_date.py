from stark.core.parsing import Pattern,ParseError
from stark.core.types import Object
from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString



from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_month import NLMonth
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_year import NLYear
from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber

from datetime import datetime

class NLCalendarDate(Object):
    value: str
    day: NLNumber | None = None
    month: NLMonth | None = None
    year: NLYear | None = None

    now = datetime.now()

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$day:NLNumber( $month:NLMonth( $year:NLYear))?")

    async def did_parse(self, from_string: LocaleString) -> str:
        
        if self.month is None:
            self.month = self.now.month

        if self.year is None:
            self.year = self.now.year

        self.value = f"{self.day:02d}.{self.month:02d}.{self.year}"
        return from_string

    def resolve(self):
        return datetime.strptime(self.value,"%d.%m.%Y")

pattern_parser.register_parameter_type(NLCalendarDate)