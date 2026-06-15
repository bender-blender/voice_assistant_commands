from voice_commands.nl_types.parsing_context import pattern_parser
from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern
from stark.core.types import Object
from datetime import datetime


class NLNow(Object):
    value: datetime

    @classproperty
    def pattern(cls):
        return Pattern("(сейчас|now)")
    
    async def did_parse(self, from_string):
        self.value = datetime.now()
        return from_string
    

pattern_parser.register_parameter_type(NLNow)