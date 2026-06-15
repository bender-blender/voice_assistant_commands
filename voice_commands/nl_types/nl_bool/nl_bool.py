from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from stark.core.types import Object

from voice_commands.nl_types.nl_bool.nl_bool_delegate import NLBoolDelegate

class NLBool(Object):

    value: bool

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")
    

    async def did_parse(self, from_string: str) -> str:
        delegate_parse = NLBoolDelegate().parse(from_string)
        
        parsed_str, parsed_bool = delegate_parse #type: ignore
        self.value = parsed_bool
        return parsed_str
        
