from stark.core.patterns import Pattern, ParseError
from stark.core.types import Object
from stark.general.classproperty import classproperty
from fb_duckling import Duckling
from deep_translator import GoogleTranslator
from voice_commands.helpers.helpers import word2num
from voice_commands.helpers.help_with_numbers import (
    get_part,
    get_a_fraction,
    multipliers,
    get_half)



class NLNumber(Object):
    value: float | None
    is_ordinal: bool
    
    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")
    
    async def did_parse(self, from_string: str) -> str:
        translate = GoogleTranslator(source="auto",target="ru").translate(from_string)
        duckling = Duckling(locale="ru_RU")
        words = translate.lower().replace(".", "")
        split_line = words.split()
    
        
        result = duckling(words)
        ordinal = [o["dim"] for o in result]
        num = [r["value"]["value"]
               for r in result if not isinstance(r["value"]["value"], str)]

        self.is_ordinal = True if ordinal and ordinal[0] == "ordinal" else False
            
        if get_a_fraction(num, split_line):
            self.value = round(get_a_fraction(num, split_line),2) #type:ignore
            print(f"{from_string} прошел с функцией дробей")
            return from_string
        
        
        if get_part(num, split_line):
            self.value = round(get_part(num, split_line),2) #type:ignore
            print(f"{from_string} прошел с функцией частей")
            return from_string
        


        half = get_half(num, split_line)
        if half:
            self.value = round(half,2)
            print(f"{from_string} прошел с функцией половин")
            return from_string
        

        for word in split_line:
            if word in multipliers and len(num) == 1:
                print("С тысячами")
                self.value = num[0] * multipliers.get(word)
                return from_string
        
        # Порядковые или простые дроби
        if len(num) == 1:
            self.value = num[0]
            return from_string


        composite = word2num(translate, "ru")
        if composite:
            self.value = composite
            return from_string
        
        

        
        raise ParseError("not found number")
        
        

