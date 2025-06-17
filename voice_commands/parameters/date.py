from datetime import datetime
from stark.core.types import Object, Pattern, classproperty


class Date(Object):

    datetime: datetime

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string: str) -> str:

        # TODO:
            # 1. extract date from `from_string`
            # 2. parse it to datetime

        return from_string

Pattern.add_parameter_type(Date)
