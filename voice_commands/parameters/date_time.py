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
        if not from_string:
            raise ParseError(f"Не удалось распознать дату/время из строки: {from_string}")

        *string, date = search_dates(from_string)
        self.value = date[1]
        return from_string

Pattern.add_parameter_type(DateTime)