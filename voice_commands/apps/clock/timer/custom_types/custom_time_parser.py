from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from dateparser import parse


from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from dateparser import parse
from datetime import datetime

class CustomTimeParser(Object):
    
    raw_input: String
    value: datetime 

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$raw_input:String")
    
    async def did_parse(self, from_string) -> str:
        parsed = parse(f"через {from_string}")
        if not parsed:
            raise ParseError(f"Не удалось распознать время из строки: {from_string}")
        
        self.raw_input = from_string # type: ignore
        self.value = parsed 
        return from_string   
    
Pattern.add_parameter_type(CustomTimeParser)