from fb_duckling import Duckling

from voice_commands.nl_types.nl_number.num_ru import multipliers

from typing import Callable, Union, NamedTuple



class Number(NamedTuple):
    value: float | int
    ordinal: bool



def delete_unit(pharse:str,locale:str = "en_US"):
    """
    Remove a unit from a string. This is necessary for proper substring removal. 
    The Number class should return only numbers.
    """
    duck = Duckling(locale=locale)
    parse:list[dict] = duck(pharse)
    if "unit" in parse[0]["value"]:
        part_string = pharse.split()
        part_string.pop()
        return delete_unit(" ".join(part_string),locale)
        
    return parse[0]["body"]



def parse_duckling(pharse: str, lang_code:str = "en_US", block_unit:bool = False) -> tuple[Number,str] | None:
    """Extracting numbers using Duckling

    Args:
        pharse (str): _description_
        lang_code (str, optional): _description_. Defaults to "en_US".
        block_unit (bool, optional): if True, remove unit from parsing. Defaults to False.

    Returns:
        tuple[Number,str] | None: return the number and the substring
    """
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
    
    if block_unit:
        substring = delete_unit(pharse,lang_code)
        return Number(number_list[0], ordinal), substring
    

    if len(number_list) == 1:
        return Number(number_list[0], ordinal), substring

    return None



pattern = Callable[[list[int | float],list[str]],Union[tuple[float,str],None]]

def parse_custom(
        pharse: str, 
        func_fraction:pattern | None = None, 
        func_part: pattern | None = None,
        func_half: pattern | None = None,
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

    half = func_half(number_list, pharse.split()) if func_half else None
    if half:
        return Number(half[0], ordinal), half[1]
    
    if lang_code == "ru_RU":
        for word in pharse.split():
            if word in multipliers and len(number_list) == 1:
                thousand = number_list[0] * multipliers.get(word)
                return Number(thousand, ordinal),substring
    return None