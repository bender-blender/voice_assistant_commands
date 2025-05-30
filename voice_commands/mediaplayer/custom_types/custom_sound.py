from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from ...helpers.helpers import word2num
from translate import Translator


class Sound(Object):

    volume: String

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$volume:String")
    
    async def did_parse(self, from_string) -> str:
        try:
            self.volume = word2num(Translator(to_lang="en", from_lang="ru").translate(from_string))
        except ValueError as e:
            raise ParseError(f"Ошибка при преобразовании слова в число: {e}")
        
        if not (0 <= self.volume <= 99):
            raise ParseError("Громкость должна быть в диапазоне от 0 до 99.")
        
        return str(self.volume)

Pattern.add_parameter_type(Sound)