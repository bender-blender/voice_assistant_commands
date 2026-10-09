from datetime import datetime

from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString
from stark.core.parsing import Pattern,ParseError
from stark.core.types import Object


from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber


class NLYear(Object):
    value: int
    century: int

    year: NLNumber
    year_part: NLNumber | None = None

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(
            "$year:NLNumber"
            "( $year_part:NLNumber)?"
            "( (год*|year*))?"
        )

    def normal_year(self, year: int) -> int:
        current_year = datetime.now().year

        if year >= 100:
            return year

        current_century = current_year // 100 * 100

        full_year = current_century + year

        if full_year > current_year:
            full_year -= 100

        return full_year

    def calculate_century(self,year: int) -> int:
        return (year - 1) // 100 + 1

    async def did_parse(self,from_string: LocaleString) -> str:
        
        if self.year is None:
            raise ParseError("year not found")
        
        year = int(self.year.value)

        if self.year_part is not None:
            second = int(self.year_part.value)

            if year < 100 and second < 100:
                year = year * 100 + second

        self.value = self.normal_year(year)

        self.century = self.calculate_century(self.value)

        return from_string


pattern_parser.register_parameter_type(
    NLYear
)