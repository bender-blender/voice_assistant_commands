from stark.core.parsing import Pattern
from stark.core.types import NLObject
from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString


from voice_commands.nl_types.nl_datetime.reusable_types.nl_datatime_components import NLDateComponents
from voice_commands.nl_types.parsing_context import pattern_parser
from datetime import datetime
from typing import Literal


class NLDatetimeStamp(NLObject):
    
    value: datetime
    component: NLDateComponents
    
    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$component:NLDateComponents")
    
    async def did_parse(self, from_string: LocaleString) -> str:
        self.value = self.component.value
        return from_string

    def resolve(self,mode: Literal["Last", "This", "Next"] = "This"):
        return self.component.resolve(mode)

pattern_parser.register_parameter_type(NLDatetimeStamp)