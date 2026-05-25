from fb_duckling import Duckling

from voice_commands.nl_types.nl_number.num_ru import multipliers

from typing import Callable, Union, NamedTuple



class Number(NamedTuple):
    value: float | int
    ordinal: bool



def parse_duckling(pharse: str, lang_code:str = "en_US") -> tuple[Number,str] | None:
    duckling_parse = Duckling(locale=lang_code)
    result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
    number_list: list[int | float] = [
        i["value"]["value"]
        for i in result_parse
        if not isinstance(i["value"]["value"], str)
    ]
    ordinal_list = [o["dim"] for o in result_parse]
    ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False
    substring = " ".join([string["body"] for string in result_parse])
    if len(number_list) == 1:
        return Number(number_list[0], ordinal), substring

    return None



#pattern = Callable[[list[int | float],list[str]],Union[tuple[float,str],None]]

def parse_custom(
        pharse: str, 
        func_fraction = None, 
        func_part = None,
        func_half = None,
        lang_code:str = "en_US") -> tuple[Number,str] | None:
    
    duckling_parse = Duckling(locale=lang_code)
    result_parse: list[dict] = duckling_parse(pharse)  # type:ignore
    number_list = [
        i["value"]["value"]
        for i in result_parse
        if not isinstance(i["value"]["value"], str)
    ]
    substring = " ".join([string["body"] for string in result_parse])
    ordinal_list = [o["dim"] for o in result_parse]
    ordinal = True if ordinal_list and ordinal_list[0] == "ordinal" else False
    fraction = func_fraction(number_list, pharse.split()) if func_fraction else None
    if fraction:
        return Number(fraction[0], ordinal), fraction[1]

    part = func_part(number_list, pharse.split()) if func_part else None
    if part:
        return Number(part[0], ordinal), part[1]
    
    half = func_half(number_list,pharse.split()) if func_half else None
    if half:
        return Number(half[0], ordinal), half[1]
    
    if lang_code == "ru_RU":
        for word in pharse.split():
            if word in multipliers and len(number_list) == 1:
                thousand = number_list[0] * multipliers.get(word)
                return Number(thousand, ordinal),substring
    return None