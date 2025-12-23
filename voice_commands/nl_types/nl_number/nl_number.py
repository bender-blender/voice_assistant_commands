from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from stark.core.types import Object

from voice_commands.nl_types.nl_number.nl_number_delegate import NLNumberDelegate



class NLNumber(Object):
    
    value: float
    is_ordinal: bool

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")
    

    async def did_parse(self, from_string: str) -> str:
        delegate = NLNumberDelegate().parse(from_string)
        self.value = round(delegate[0],2) #type: ignore
        self.is_ordinal = delegate[1] #type: ignore
        return from_string
