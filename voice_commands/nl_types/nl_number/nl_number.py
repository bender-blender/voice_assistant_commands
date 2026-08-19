from stark.core.parsing import Pattern, ParseError
from stark.general.classproperty import classproperty
from stark.core.types import Object

from .number_miltilang import NLMultiNumber
from .number_ru import NLNumberRU
from voice_commands.nl_types.parsing_context import pattern_parser


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

    async def did_parse(self, from_string):
        last_error = None

        for parser_class in self.parsers:
            parser = parser_class()

            try:
                substring = await parser.did_parse(from_string)

                self.value = parser.value
                self.is_ordinal = parser.is_ordinal

                return substring

            except (ParseError, ValueError, TypeError) as error:
                last_error = error

        raise ParseError(
            f"Number not found: {from_string!r}"
        ) from last_error
    
pattern_parser.register_parameter_type(NLNumber)