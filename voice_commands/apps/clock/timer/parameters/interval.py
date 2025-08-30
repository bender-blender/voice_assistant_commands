from datetime import datetime

import dateparser
from stark.core.patterns import Pattern
from stark.core.types import Object, ParseError
from stark.general.classproperty import classproperty


class Interval(Object):
    value: datetime | None

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string: str) -> str:
        parsing = dateparser.parse(from_string)
        current_date = datetime.now()
        if parsing is None:
            raise ParseError("Failed to parse interval")
        

        if parsing <= current_date:
            self.value = current_date + (current_date - parsing)
            return from_string

        raise ParseError("the time indicated is past")


Pattern.add_parameter_type(Interval)
