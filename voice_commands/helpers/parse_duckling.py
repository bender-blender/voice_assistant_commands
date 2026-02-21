from fb_duckling import Duckling

from voice_commands.helpers.num_ru import multipliers

from typing import Callable, Union, NamedTuple



class Number(NamedTuple):
    value: float | int
    ordinal: bool



def parse_duckling(pharse: str, lang_code:str = "en_US") -> Number | None:
    duckling_parse = Duckling(locale=lang_code)
    result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
    number_list: list[int | float] = [
        i["value"]["value"]
        for i in result_parse
        if not isinstance(i["value"]["value"], str)
    ]
    ordinal_list = [o["dim"] for o in result_parse]
    ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False
    if len(number_list) == 1:
        return Number(number_list[0], ordinal)

    return None



pattern = Callable[[list[int | float],list[str]],Union[float,None]]

def parse_custom(
        pharse: str, 
        func_fraction:pattern, 
        func_part: pattern,
        func_half: pattern,
        lang_code:str = "en_US") -> Number | None:
    
    duckling_parse = Duckling(locale=lang_code)
    result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
    number_list = [
        i["value"]["value"]
        for i in result_parse
        if not isinstance(i["value"]["value"], str)
    ]
   
    
    ordinal_list = [o["dim"] for o in result_parse]
    ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False
    fraction = func_fraction(number_list, pharse.split())
    if fraction:
        return Number(fraction, ordinal)

    part = func_part(number_list, pharse.split())
    if part:
        return Number(part, ordinal)

    half = func_half(number_list, pharse.split())
    if half:
        return Number(half, ordinal)
    
    if lang_code == "ru_RU":
        for word in pharse.split():
            if word in multipliers and len(number_list) == 1:
                thousand = number_list[0] * multipliers.get(word)
                return Number(thousand, ordinal)
    return None