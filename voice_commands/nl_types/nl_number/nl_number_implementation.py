from typing import Tuple
import ru_word2number.w2n
from word2number.w2n import word_to_num



from voice_commands.nl_types.nl_number.nl_number_interface import (
    NLNumberParseCustom,
    NLNumberParserDucklingTranslated,
    NLNumberParseWordToNum
)

from voice_commands.helpers.help_with_numbers import (
    get_a_fraction,
    get_a_fraction_en,
    get_part,
    #get_a_part_en,
    get_half,
    get_half_en,
)
from voice_commands.helpers.parse_duckling import (
    parse_duckling,
    parse_custom,
    Number
)



class NLNumberParseWordToNumRu(NLNumberParseWordToNum):
    def parse(self, pharse: str) -> Tuple[Number, str] | None:
        substring = []
        for word in pharse.split():
            try:
                ru_word2number.w2n.word_to_num(word)
                substring.append(word)
            except ValueError:
                continue
        
        if len(substring) == 0:
            return None
        glue_string = " ".join(substring)
        return Number(ru_word2number.w2n.word_to_num(glue_string), False ), glue_string


class NLNumberParseWordToNumEn(NLNumberParseWordToNum):
    def parse(self, pharse: str) -> Tuple[Number, str] | None:
        substring = []
        for word in pharse.split():
            try:
                word_to_num(word)
                substring.append(word)
            except ValueError:
                continue
        
        if len(substring) == 0:
            return None
        
        glue_string = " ".join(substring)
        return Number(word_to_num(glue_string), False), glue_string
        

        

class NLNumberParserDucklingTranslatedRu(NLNumberParserDucklingTranslated):

    def parse(self, pharse: str) -> Tuple[Number,str] | None:
        duckling_parse = parse_duckling(pharse,"ru_RU")
        if duckling_parse:
            print(f"Парсится с duckling ru : {pharse}")
            return duckling_parse
        return None


class NLNumberParserDucklingTranslatedEn(NLNumberParserDucklingTranslated):
    
    def parse(self, pharse: str) -> Tuple[Number,str] | None | None:
        duckling_parse = parse_duckling(pharse)
        if duckling_parse:
            return duckling_parse
        return None



class NLNumberParseCustomRu(NLNumberParseCustom):
    
    def _get_fraction(self, list_num: list[int | float], pharse: list[str]):
        parse_fraction = get_a_fraction(list_num,pharse)
        if parse_fraction:
            return parse_fraction
        return None
    
    def _get_half(self, list_num: list[float | int], pharse: list[str]):
        parse_half = get_half(list_num,pharse)
        if parse_half:
            return parse_half
        return None
    
    def _get_part(self, list_num:list[float|int], pharse: list[str]):
        parse_part = get_part(list_num,pharse)
        if parse_part:
            return parse_part
        return None

    def parse(self, pharse: str):
        duckling_parse = parse_custom(
            pharse=pharse,
            func_fraction=self._get_fraction,
            func_part=self._get_part,
            func_half=self._get_half,
            lang_code="ru_RU")
        if duckling_parse:
            return duckling_parse
        return None


class NLNumberParseCustomEn(NLNumberParseCustom):
    
    def _get_fraction(self, list_num: list[int | float], pharse: list[str]) -> tuple[float, str] | None:
        parse_fraction = get_a_fraction_en(list_num,pharse)
        if parse_fraction:
            return parse_fraction
        return None
        
    def _get_half(self, list_num: list[int | float], pharse: list[str]) -> tuple[float, str] | None:
        parse_half = get_half_en(list_num,pharse)
        if parse_half:
            return parse_half
        return None
    
    def parse(self, pharse: str) -> tuple[Number, str] | None:
        duckling_parse = parse_custom(
            pharse=pharse,
            func_fraction=self._get_fraction,
            func_half=self._get_half
        )
        if duckling_parse:
            return duckling_parse
        return None