# TODO: Implement custom class
from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from dateparser import parse


class TimeInterval(Object):
    
    value: String

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$value:String")
    
    async def did_parse(self, from_string) -> str:
        parsed = parse(f"через {from_string}")
        if not parsed:
            raise ParseError(f"Не удалось распознать время из строки: {from_string}")
        
        self.value = parsed # type: ignore
        return from_string   
    
Pattern.add_parameter_type(TimeInterval)