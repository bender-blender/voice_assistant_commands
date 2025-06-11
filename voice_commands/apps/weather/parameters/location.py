from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from dataclasses import dataclass
from translate import Translator
import requests


# @dataclass
class Location(Object):

    location: String

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$location:String")

    async def did_parse(self, from_string: str) -> str:
        if not from_string:
            raise ParseError("Город не указан")

        #print("[DEBUG] from_string:", repr(from_string))
        from_string = from_string.strip()
        translator = Translator(to_lang="en", from_lang="ru")
        translated_city = translator.translate(from_string.title())

        #print("[DEBUG] translated_city:", translated_city)

        self.location = translated_city

        #print("[DEBUG] self.terrain set to:", self.terrain)

        return from_string

Pattern.add_parameter_type(Location)
