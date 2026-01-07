from .num_ru import fractions,half
from .num_en import fraction_en,half_en


def get_part(list_num: list[int | float], line: list[str]) -> None | float:
    # Для частей
    part = [fractions[i] for i in line if i in fractions]
    if part and len(list_num) != 0:
        return list_num[0] * part[0]

    elif part and len(list_num) == 0:
        return part[0]

    return None


def get_a_fraction(list_num: list[int | float], line: list[str]) -> float | None:
    if not list_num:
        return None

    # тип "три точка четырнадцать"
    point_words = ["точка"]
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


#---------------------------------------------------


def get_half_en(list_num: list[int | float], line: list[str]) -> None | float:
    print(list_num)
    for key in half_en:


        if key in line and len(list_num) == 0:
            return half_en[key]
        
        if key in line and len(list_num) == 1:
            return list_num[0] + half_en[key]
        
    return None


def get_a_part_en(list_num: list[int | float],line:list[str]):
    if not list_num:
        return None
    
    for i in list_num:
        if isinstance(i,float):
            return -i if "minus" in line else i
    

def get_a_fraction_en(list_num: list[int | float], line:list[str]):
    if "point" not in line:
        return None

    string_assembly = ""
    for i in list_num:
        string_assembly += str(i)
    return string_assembly