from fb_duckling import Duckling
from typing import Tuple
import ru_word2number.w2n
from word2number.w2n import word_to_num



from voice_commands.nl_types.nl_number.nl_number_interface import (
    NLNumberParseCustom,
    NLNumberParserDucklingTranslated,
    NLNumberParseWordToNum
)




class NLNumberParseWordToNumRu(NLNumberParseWordToNum):
    def parse(self, pharse: str) -> tuple[int | float, bool] | None:
        try:
            number = ru_word2number.w2n.word_to_num(pharse)
            return number, False
        except ValueError:
            return None


class NLNumberParseWordToNumEn(NLNumberParseWordToNum):
    def parse(self, pharse: str) -> tuple[int | float, bool] | None:
        try:
            number = word_to_num(pharse)
            return number, False
        except ValueError:
            return None
        

class NLNumberParserDucklingTranslatedRu(NLNumberParserDucklingTranslated):

    def parse(self, pharse: str) -> Tuple[float | int, bool] | None:
        duckling_parse = Duckling(locale="ru_RU")
        result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
        number_list = [
            i["value"]["value"]
            for i in result_parse
            if not isinstance(i["value"]["value"], str)
        ]
        ordinal_list = [o["dim"] for o in result_parse]
        ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False

        if len(number_list) == 1:
            return number_list[0], ordinal
        else:
            return None


class NLNumberParserDucklingTranslatedEn(NLNumberParserDucklingTranslated):
    
    def parse(self, pharse: str) -> Tuple[float, bool] | None:
        duckling_parse = Duckling(locale="en_US")
        result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
        number_list: list[int | float] = [
            i["value"]["value"]
            for i in result_parse
            if not isinstance(i["value"]["value"], str)
        ]

        ordinal_list = [o["dim"] for o in result_parse]
        ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False

        if len(number_list) == 1:
            return number_list[0], ordinal

        return None




class NLNumberParseCustomRu(NLNumberParseCustom):
    
    def __init__(self) -> None:
        self.fractions = {
            "четверть": 0.25, "четверти": 0.25,
            "треть": 0.333, "трети": 0.333,
            "третья часть": 0.333, "четвертая часть": 0.25,
            "одна треть": 0.333, "одна четверть": 0.25,
        }

        self.half = {"половина": 0.5, "половины": 0.5, "половиной": 0.5,
                "половинку": 0.5, "наполовину": 0.5}
        
        self.multipliers = {
            "тысяча": 1000,
            "тысяч": 1000,
            "тысячи": 1000,
            "миллион": 1000000,
            "миллиона": 1000000,
            "миллионов": 1000000,
            "миллиард": 1000000000,
            "миллиарда": 1000000000,
            "миллиардов": 1000000000,
        }

    def _get_fraction(self, list_num: list[int | float], pharse: list[str]):
        if not list_num:
            return None

        # тип "три точка четырнадцать"
        point_words = ["точка"]
        if any(p in pharse for p in point_words) and len(list_num) >= 2:
            integer_part = int(list_num[0])
            decimal_part = ''.join(str(int(x)) for x in list_num[1:])
            return float(f"{integer_part}.{decimal_part}")

        # тип "один и шесть" или "два целых пять"
        fraction_words = ["и", "целых"]
        if any(e in pharse for e in fraction_words):
            if len(list_num) == 2:
                integer_part = int(list_num[0])
                decimal_part_num = int(list_num[1])
                decimal_part_str = str(decimal_part_num)
                return float(f"{integer_part}.{decimal_part_str}")
            elif len(list_num) > 2:
                return list_num[0] + list_num[1] / list_num[2]

        # тип "пять десятых", "четырнадцать сотых", "одна вторая"
        endings = ["ых", "ая"]
        if any(pharse[-1].endswith(end) for end in endings):
            if len(list_num) == 3:
                return list_num[0] + list_num[1] / list_num[2]
            elif len(list_num) == 2:
                return list_num[0] / list_num[1]

        return None
    
    def _get_half(self, list_num: list[float | int], pharse: list[str]):
        for key in self.half:

            if key in pharse and len(pharse) == 1:
                return self.half[key]
            elif key in pharse and len(pharse) > 1:
                return list_num[0]

        return None
    
    def _get_part(self, list_num:list[float|int], pharse: list[str]):
        part = [self.fractions[i] for i in pharse if i in self.fractions]
        if part and len(list_num) != 0:
            return list_num[0] * part[0]

        elif part and len(list_num) == 0:
            return part[0]

        return None

    def parse(self, pharse: str):
        duckling_parse = Duckling(locale="ru_RU")
        result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
        number_list = [
            i["value"]["value"]
            for i in result_parse
            if not isinstance(i["value"]["value"], str)
        ]
        ordinal_list = [o["dim"] for o in result_parse]
        ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False

        fraction = self._get_fraction(number_list, pharse.split())
        if fraction:
            return fraction, ordinal

        part = self._get_part(number_list, pharse.split())
        if part:
            return part, ordinal

        half = self._get_half(number_list, pharse.split())
        if half:
            return half, ordinal

        for word in pharse.split():
            if word in self.multipliers and len(number_list) == 1:
                thousand = number_list[0] * self.multipliers.get(word)
                return thousand, ordinal

        return None


class NLNumberParseCustomEn(NLNumberParseCustom):

    def __init__(self) -> None:
        self.fraction = {"quarter": 0.25, "a quarter": 0.25, "one quarter": 0.25,
                        "third": 0.333, "a third": 0.333, "one third": 0.333,
                        "fourth": 0.25, "a fourth": 0.25, "one fourth": 0.25, }

        self.half = {"half": 0.5, "a half": 0.5, "one half": 0.5}
    
    def _get_fraction(self, list_num: list[int | float], pharse: list[str]) -> str | None:
        if "point" not in pharse:
            return None

        string_assembly = ""
        for i in list_num:
            string_assembly += str(i)
        return string_assembly
        
    def _get_half(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        for key in self.half:

            if key in pharse and len(list_num) == 0:
                return self.half[key]

            if key in pharse and len(list_num) == 1:
                return list_num[0] + self.half[key]

        return None
    
    def _get_part(self, list_num: list[int | float], pharse: list[str]) -> float | None:
        if not list_num:
            return None

        for i in list_num:
            if isinstance(i, float):
                return -i if "minus" in pharse else i
        
        return None
        
    
    def parse(self, pharse: str) -> Tuple[float, bool] | None:
        duckling_parse = Duckling(locale="en_US")
        result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
        number_list = [
            i["value"]["value"]
            for i in result_parse
            if not isinstance(i["value"]["value"], str)
        ]
        ordinal_list = [o["dim"] for o in result_parse]
        ordinal = True if (
            ordinal_list and ordinal_list[0] == "ordinal") else False
        
        fraction = self._get_fraction(number_list, pharse.split())
        if fraction:
            return float(fraction), ordinal

        part = self._get_part(number_list, pharse.split())
        if part:
            return part, ordinal

        half = self._get_half(number_list, pharse.split())
        if half:
            return half, ordinal

        return None
