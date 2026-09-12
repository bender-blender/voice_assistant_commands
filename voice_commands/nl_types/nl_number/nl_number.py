from stark.core.parsing import Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object

from .number_miltilang import NLMultiNumber
from .number_ru import NLNumberRU
from voice_commands.nl_types.parsing_context import pattern_parser
from fb_duckling import Duckling

class NLNumber(Object):
    value: float
    is_ordinal: bool

    parsers = (
        NLMultiNumber,
        NLNumberRU,
    )

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")


    def parse_duck(self,locale:str,from_string:str):
        duck = Duckling(locale=locale)
        parse = duck(from_string)
        print(parse)
        if parse:
            return parse[0]["value"]["value"],parse[0]["body"]


    async def did_parse(self, from_string):
        last_error = None

        for parser_class in self.parsers:
            try:
                parsed = await pattern_parser.parse_object(
                    parser_class,
                    from_string,
                )

                self.value = parsed.obj.value
                self.is_ordinal = parsed.obj.is_ordinal

                return parsed.substring

            except (ParseError, ValueError, TypeError) as error:
                last_error = error
                continue


        for locale in ("ru_RU", "en_US"):
            duck_result = self.parse_duck(locale, from_string)

            if duck_result:
                self.value = duck_result[0]
                self.is_ordinal = False
                return duck_result[1]

        raise ParseError(
            f"Number not found: {from_string!r}"
        ) from last_error
    
pattern_parser.register_parameter_type(NLNumber)