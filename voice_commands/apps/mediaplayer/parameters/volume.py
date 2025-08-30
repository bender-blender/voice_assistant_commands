from stark.core.patterns import Pattern
from stark.core.types import Object, ParseError
from stark.general.classproperty import classproperty
from translate import Translator

from ....helpers.helpers import word2num


class Volume(Object):
    value: str

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string) -> str:
        try:
            sound = word2num(Translator(to_lang="en", from_lang="ru").translate(from_string),lang="ru")  # type: ignore
        except ValueError as e:
            raise ParseError(f"Ошибка при преобразовании слова в число: {e}")

        if not (0 <= sound <= 99):  # type: ignore
            raise ParseError("Громкость должна быть в диапазоне от 0 до 99.")

        self.value = str(sound)  # type: ignore
        return from_string


Pattern.add_parameter_type(Volume)
