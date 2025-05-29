from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from dateparser import parse


class CustomTimeParser(Object):
    
    raw_input: String

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$raw_input:String")
    
    async def did_parse(self, from_string) -> str:
        parsed_time = parse(f"через {from_string}")
        if not parsed_time:
            raise ParseError(f"Не удалось распознать время из строки: {self.raw_input}")
        
        self.raw_input = parsed_time  
        return str(parsed_time)

    
Pattern.add_parameter_type(CustomTimeParser)