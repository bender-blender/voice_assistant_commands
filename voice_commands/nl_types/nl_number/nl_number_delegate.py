from stark.core.patterns import ParseError
from voice_commands.nl_types.nl_number.nl_number_implementation import (
    NLNumberParseCustomEn,
    NLNumberParseCustomRu,
    NLNumberParserDucklingTranslatedEn,
    NLNumberParserDucklingTranslatedRu,
    NLNumberParseWordToNumEn,
    NLNumberParseWordToNumRu
)
from typing import Tuple

from voice_commands.nl_types.nl_number.nl_number_interface import (
    NLNumberParseCustom,
    NLNumberParserDucklingTranslated,
    NLNumberParseWordToNum
)

from voice_commands.helpers.detect_lang import identify_the_language

class NLNumberDelegate:

    def __init__(self) -> None:
        self.language_parsers: dict[str, Tuple[NLNumberParseCustom, NLNumberParserDucklingTranslated, NLNumberParseWordToNum]] = {
            "ru": (
                NLNumberParseCustomRu(), 
                NLNumberParserDucklingTranslatedRu(),
                NLNumberParseWordToNumRu()),
            "en": (
                NLNumberParseCustomEn(),
                NLNumberParserDucklingTranslatedEn(),
                NLNumberParseWordToNumEn()
            )
        }
    
    def parse(self, from_string: str) -> Tuple[float, bool] | None:
        lang = identify_the_language(from_string)

        parsers = self.language_parsers.get(lang)  # type: ignore
        
        if not parsers:
            raise ParseError(f'Unsupported language: {lang}')
        
        for parser in parsers:
            parsing_stages = parser.parse(from_string)
            if parsing_stages:
                return parsing_stages
        return None
        

