from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern
from stark.core.types import NLObject
from pint import Unit



class NLAbstractUnit(NLObject):
    value: Unit    
    _unit_keywords: str
    key: Unit
    
    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(cls._unit_keywords)

    async def did_parse(self, from_string):
        self.value = self.key
        return from_string

