from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern
from stark.core.types import Object

from datetime import datetime

from stark.general.localisation import LocaleString

from voice_commands.nl_types.parsing_context import pattern_parser

class NL_Now(Object):

    value:datetime


    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("(сейчас|now)")


    async def did_parse(self, from_string: LocaleString) -> str:
        self.value = datetime.now()
        return from_string

pattern_parser.register_parameter_type(NL_Now)