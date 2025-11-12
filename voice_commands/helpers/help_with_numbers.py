from .fractions_ru import fractions
from .fractions_ru import half
from .helpers import word2num


def get_part(list_num:list[int|float], line:list[str]) -> None | float:
    # Для частей
    part = [fractions[i] for i in line if i in fractions]
    if part and len(list_num) != 0:
        return list_num[0] * part[0]
        
    elif part and len(list_num) == 0:
        return part[0]
    
    return None
        

def get_a_fraction(list_num: list[int | float], line: list[str]) -> float | None:
    """
    Универсальная функция для дробей:
    - "три точка четырнадцать" / "three point one four" -> 3.14
    - "два целых пять десятых" / "two and five tenths" -> 2.5
    - "один и шесть" -> 1.6
    - "четырнадцать сотых" -> 0.14
    - "одна вторая" -> 0.5
    """
    if not list_num:
        return None

    # тип "три точка четырнадцать"
    point_words = ["точка", "очка"]
    if any(p in line for p in point_words) and len(list_num) >= 2:  
        integer_part = int(list_num[0])
        decimal_part = ''.join(str(int(x)) for x in list_num[1:])
        return float(f"{integer_part}.{decimal_part}")

    # тип "один и шесть" или "два целых пять"
    fraction_words = ["и", "целых"]
    if any(e in line for e in fraction_words):
        if len(list_num) == 2:
            integer_part = int(list_num[0])
            decimal_part_num = int(list_num[1])
            decimal_part_str = str(decimal_part_num)
            return float(f"{integer_part}.{decimal_part_str}")
        elif len(list_num) > 2:
            return list_num[0] + list_num[1] / list_num[2]

    # тип "пять десятых", "четырнадцать сотых", "одна вторая"
    endings = ["ых", "ая"]
    if any(line[-1].endswith(end) for end in endings):
        if len(list_num) == 3:
            return list_num[0] + list_num[1] / list_num[2]
        elif len(list_num) == 2:
            return list_num[0] / list_num[1]

    return None





def get_half(list_num: list[int | float], line: list[str]) -> None | float:
    # Для половин
    for key in half:
        
        if key in line and len(line) == 1:
            return half[key]
        elif key in line and len(line) > 1:
            return list_num[0]

    return None


multipliers = {
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


