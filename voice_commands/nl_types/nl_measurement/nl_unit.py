from stark.general.classproperty import classproperty
from stark.core.parsing import Pattern
from stark.core.types import Object
from pint import Unit



class NLAbstractUnit(Object):
    value: Unit
    
    _unit_keywords: str

    key: Unit


    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(f"{cls._unit_keywords}")

    async def did_parse(self, from_string):
        self.value = self.key
        return from_string

