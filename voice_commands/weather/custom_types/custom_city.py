from stark.core.types import Object, String, ParseError
from stark.general.classproperty import classproperty
from stark.core.patterns import Pattern
from dataclasses import dataclass
from translate import Translator


@dataclass
class CustomCity(Object):
    terrain: String

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("$terrain:String")
    
    async def did_parse(self, from_string: str) -> str:
        if not from_string:
            raise ParseError("Город не указан")

        #print("[DEBUG] from_string:", repr(from_string))
        from_string = from_string.strip().title()
        translator = Translator(to_lang="en", from_lang="ru")
        translated_city = translator.translate(from_string)

        #print("[DEBUG] translated_city:", translated_city)

        self.terrain = translated_city

        #print("[DEBUG] self.terrain set to:", self.terrain)

        return self.terrain




# from stark.core.types import Object, String, ParseError
# from stark.general.classproperty import classproperty
# from stark.core.patterns import Pattern
# from dataclasses import dataclass
# from translate import Translator




# @dataclass
# class CustomCity(Object):
#     terrain: String

#     @classproperty
#     def pattern(cls) -> Pattern:
#         return Pattern("$terrain:String")
    
#     async def did_parse(self, from_string: str) -> str:
#         if not from_string:
#             raise ParseError("Город не указан")
    
#         translator = Translator(to_lang="en", from_lang="ru")
#         translated_city = translator.translate(from_string).title()
#         self.terrain = translated_city
#         return self.terrain

Pattern.add_parameter_type(CustomCity)