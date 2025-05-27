from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from .data_dictionary import GeneralDictionary

class Year(Object):
    year: String
    numbers = GeneralDictionary().words_to_numbers

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern('$year:String')

    async def did_parse(self, from_string) -> str:
        words = from_string.lower().replace("-", " ").split()

        if not words:
            raise ParseError("Не указано ни одного слова для года.")

        total = 0
        
        for word in words:
            if word in self.numbers:
                total += self.numbers[word]

        self.year = str(total)
        return self.year
    
Pattern.add_parameter_type(Year)