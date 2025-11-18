from stark.core.patterns import Pattern, ParseError
from stark.core.types import Object
from stark.general.classproperty import classproperty
from .nl_number_implementation import (
    NLNumberParserDucklingTranslatedRu,
    NLNumberParserWord2NumRu,
    NLNumberParseCustomRu,
    NLNumberParserDucklingTranslatedEn,
    NLNumberParserWord2NumEn,
    NLNumberParseCustomEn
)

from voice_commands.helpers.detect_lang import identify_the_language


class NLNumber(Object):
    value: float
    is_ordinal: bool

    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")

    async def did_parse(self, from_string: str) -> str:
        lang = identify_the_language(from_string)
        if lang == "ru":

            custom = NLNumberParseCustomRu(from_string, lang).parse()
            if custom:
                self.value = round(custom[0],2)
                self.is_ordinal = custom[1]
                return from_string

            duckling = NLNumberParserDucklingTranslatedRu(from_string).parse()
            if duckling:
                self.value = duckling[0]
                self.is_ordinal = duckling[1]
                return from_string

            word2num = NLNumberParserWord2NumRu(from_string).parse()
            if word2num:
                self.value = word2num[0]  
                self.is_ordinal = word2num[1]
                return from_string
        
        if lang == "en":
            custom = NLNumberParseCustomEn(from_string).parse()
            if custom:
                self.value = round(custom[0], 2)
                self.is_ordinal = custom[1]
                return from_string
            
            duckling = NLNumberParserDucklingTranslatedEn(from_string).parse()
            if duckling:
                self.value = duckling[0]
                self.is_ordinal = duckling[1]
                return from_string
            
            word2num = NLNumberParserWord2NumEn(from_string).parse()
            if word2num:
                self.value = word2num[0]
                self.is_ordinal = word2num[1]
                return from_string
        

        raise ParseError("not found number")
