from datetime import datetime

from dateparser.search import search_dates
from stark.core.patterns import Pattern
from stark.core.types import Object, ParseError
from stark.general.classproperty import classproperty

from ..helpers.helpers import day_to_date, parse_day_phrase


class DateTime(Object):
    value: datetime | None

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string) -> str:
        word = from_string.split(" ")

        try:
            custom_checks = parse_day_phrase(word)
            if custom_checks:
                self.value = custom_checks[1]
                return custom_checks[0]

        except ValueError:
            custom_checks = day_to_date(word)
            if custom_checks:
                self.value = custom_checks[1]
                return custom_checks[0]

        *sting, result = search_dates(from_string)
        if result:
            self.value = result[1]
            return result[0]

        raise ParseError("Couldn't find date in line")


Pattern.add_parameter_type(DateTime)
