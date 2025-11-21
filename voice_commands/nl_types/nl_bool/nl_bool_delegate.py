from stark.core.patterns import ParseError

from typing import Tuple
from voice_commands.nl_types.nl_bool.nl_bool_implementation import NLBoolParseRu,NLBoolParseEn
from voice_commands.nl_types.nl_bool.nl_bool_interface import NLBoolParseLanguage
from voice_commands.helpers.detect_lang import identify_the_language

class NLBoolDelegate:

    def __init__(self) -> None:
        self.language_parsers:dict[str,NLBoolParseLanguage] = {"ru": NLBoolParseRu(),"en":NLBoolParseEn()}
    
    def parse(self, from_string: str) -> Tuple[str, bool] | None:
        lang = identify_the_language(from_string)
        if lang:
            parser = self.language_parsers.get(lang)
            if parser:
                return parser.parse(from_string)
        raise ParseError(f'Unsupported language: {lang}')
