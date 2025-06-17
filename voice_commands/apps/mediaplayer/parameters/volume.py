from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from ....helpers.helpers import word2num
from translate import Translator


class Volume(Object):

    value: String

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$value:String")

    async def did_parse(self, from_string) -> str:
        try:
            self.value = word2num(Translator(to_lang="en", from_lang="ru").translate(from_string)) # type: ignore
        except ValueError as e:
            raise ParseError(f"Ошибка при преобразовании слова в число: {e}")

        if not (0 <= self.value <= 99): # type: ignore
            raise ParseError("Громкость должна быть в диапазоне от 0 до 99.")
    
        self.value = str(self.value) # type: ignore
        return from_string
Pattern.add_parameter_type(Volume)