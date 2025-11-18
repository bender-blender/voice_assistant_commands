from fb_duckling import Duckling
from typing import Tuple
import ru_word2number.w2n
from word2number.w2n import word_to_num
from .nl_number_interface import NLNumberParser
from voice_commands.helpers.help_with_numbers import (
    get_a_fraction,
    get_half,
    get_part,
    get_a_part_en,
    get_half_en,
    get_a_fraction_en
)

from voice_commands.helpers.num_ru import multipliers


class NLNumberParserWord2NumRu(NLNumberParser):
    def parse(self) -> tuple[int | float, bool] | None:
        try:
            number = ru_word2number.w2n.word_to_num(self.pharse)
            return number, False
        except ValueError:
            return None


class NLNumberParserDucklingTranslatedRu(NLNumberParser):
    def parse(self) -> Tuple[float | int, bool] | None:
        duckling_parse = Duckling(locale="ru_RU")
        result_parse: list[dict] = duckling_parse(self.pharse)  # type:ignore
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


class NLNumberParseCustomRu(NLNumberParser):

    def __init__(self, pharse: str, lang: str) -> None:
        super().__init__(pharse)
        self.lang = lang

    def parse(self) -> Tuple[float, bool] | None:
        duckling_parse = Duckling(locale="ru_RU")
        result_parse: list[dict] = duckling_parse(self.pharse)  # type:ignore
        number_list = [
            i["value"]["value"]
            for i in result_parse
            if not isinstance(i["value"]["value"], str)
        ]
        ordinal_list = [o["dim"] for o in result_parse]
        ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False

        fraction = get_a_fraction(number_list, self.pharse.split())
        if fraction:
            return fraction, ordinal

        part = get_part(number_list, self.pharse.split())
        if part:
            return part, ordinal

        half = get_half(number_list, self.pharse.split())
        if half:
            return half, ordinal

        for word in self.pharse.split():
            if word in multipliers and len(number_list) == 1:
                thousand = number_list[0] * multipliers.get(word)
                return thousand, ordinal

        return None


class NLNumberParserWord2NumEn(NLNumberParser):
    def parse(self) -> tuple[int | float, bool] | None:
        try:
            number = word_to_num(self.pharse)
            return number, False
        except ValueError:
            return None


class NLNumberParserDucklingTranslatedEn(NLNumberParser):
    def parse(self) -> Tuple[float, bool] | None:
        duckling_parse = Duckling(locale="en_US")
        result_parse: list[dict] = duckling_parse(self.pharse)  # type:ignore
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


class NLNumberParseCustomEn(NLNumberParser):

    def parse(self) -> Tuple[float, bool] | None:
        duckling_parse = Duckling(locale="en_US")
        result_parse: list[dict] = duckling_parse(self.pharse)  # type:ignore
        number_list = [
            i["value"]["value"]
            for i in result_parse
            if not isinstance(i["value"]["value"], str)
        ]
        ordinal_list = [o["dim"] for o in result_parse]
        ordinal = True if (
            ordinal_list and ordinal_list[0] == "ordinal") else False


        fraction = get_a_fraction_en(number_list, self.pharse.split())
        if fraction:
            return float(fraction), ordinal

        part = get_a_part_en(number_list, self.pharse.split())
        if part:
            return part, ordinal

        half = get_half_en(number_list, self.pharse.split())
        if half:
            return half, ordinal

        return None
