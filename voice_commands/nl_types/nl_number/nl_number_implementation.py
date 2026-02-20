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
    get_a_part_en,
    get_half,
    get_half_en,
)
from voice_commands.helpers.parse_duckling import (
    parse_duckling,
    parse_custom
)



class NLNumberParseWordToNumRu(NLNumberParseWordToNum):
    def parse(self, pharse: str) -> tuple[int | float, bool] | None:
        try:
            number = ru_word2number.w2n.word_to_num(pharse)
            print(f"Парсится с word2num ru: {pharse}")
            return number, False
        except ValueError:
            return None


class NLNumberParseWordToNumEn(NLNumberParseWordToNum):
    def parse(self, pharse: str) -> tuple[int | float, bool] | None:
        try:
            number = word_to_num(pharse)
            print(f"Парсится с word2num en: {pharse}")
            return number, False
        except ValueError:
            return None
        

class NLNumberParserDucklingTranslatedRu(NLNumberParserDucklingTranslated):

    def parse(self, pharse: str) -> Tuple[float | int, bool] | None:
        duckling_parse = parse_duckling(pharse,"ru_RU")
        if duckling_parse:
            print(f"Парсится с duckling ru : {pharse}")
            return duckling_parse
        return None


class NLNumberParserDucklingTranslatedEn(NLNumberParserDucklingTranslated):
    
    def parse(self, pharse: str) -> Tuple[float, bool] | None:
        duckling_parse = parse_duckling(pharse)
        if duckling_parse:
            print(f"Парсится с duckling en : {pharse}")
            return duckling_parse
        return None



class NLNumberParseCustomRu(NLNumberParseCustom):
    
    def _get_fraction(self, list_num: list[int | float], pharse: list[str]):
        parse_fraction = get_a_fraction(list_num,pharse)
        if parse_fraction:
            print(f"Парсится с русскими дробями: {pharse}")
            return parse_fraction
        return None
    
    def _get_half(self, list_num: list[float | int], pharse: list[str]):
        parse_half = get_half(list_num,pharse)
        if parse_half:
            print(f"Парсится с русскими половинами: {pharse}")
            return parse_half
        return None
    
    def _get_part(self, list_num:list[float|int], pharse: list[str]):
        parse_part = get_part(list_num,pharse)
        if parse_part:
            print(f"Парсится с русскими частями: {pharse}")
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
    
    def _get_fraction(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        parse_fraction = get_a_fraction_en(list_num,pharse)
        if parse_fraction:
            return parse_fraction
        return None
        
    def _get_half(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        parse_half = get_half_en(list_num,pharse)
        if parse_half:
            return parse_half
        return None
    
    def _get_part(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        parse_part = get_a_part_en(list_num,pharse)
        if parse_part:
            return parse_part
        return None
        
    
    def parse(self, pharse: str) -> Tuple[float, bool] | None:
        duckling_parse = parse_custom(
            pharse=pharse,
            func_fraction=self._get_fraction,
            func_part=self._get_part,
            func_half=self._get_half
        )
        if duckling_parse:
            return duckling_parse
        return None