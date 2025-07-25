from stark.general.classproperty import classproperty
from stark.core.types import Object, ParseError
from dateparser.search import search_dates
from stark.core.patterns import Pattern
from datetime import datetime


class DateTime(Object):

    value: datetime | None

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string) -> str:

        print(f"[DEBUG] Parsing string: {from_string}")
        *string, date = search_dates(from_string)
        if date is None:
            raise ParseError("Couldn't find date in line")
        self.value = date[1]
        return date[0]


Pattern.add_parameter_type(DateTime)
