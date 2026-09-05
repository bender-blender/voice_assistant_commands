from .num_ru import fractions,half
from .num_en import half_en

def make_result(value, line, start, end) -> tuple[float, str]:
    substring = " ".join(line[start:end])
    return value, substring

def get_part(list_num: list[int | float], line: list[str]) -> tuple[float,str] | None:
    try:
        number_in_string = str(list_num[0])
    except IndexError:
        return None
    
    for i,word in enumerate(line):
        if word in fractions:
            if len(list_num) == 0:
                return make_result(fractions[word],line,i,i+1)
            
            calculation = list_num[0] * fractions[word]
            return make_result(calculation,line,i-len(number_in_string),i+1)


    return None



def get_a_fraction(list_num: list[int], line: list[str]) -> tuple[float,str] | None:
    if not list_num:
        return None

    first_number = str(list_num[0]) if list_num[0] % 10 != 0 else str(int(list_num[0] / 10))
    #second_number = str(list_num[1]) if list_num[1] % 10 != 0 else str(int(list_num[1] / 10))
    # тип "три точка четырнадцать"
    if "точка" in line and len(list_num) >= 2:
        point_index = line.index("точка")

        integer_part = int(list_num[0])
        decimal_part = ''.join(str(int(x)) for x in list_num[1:])
        value = float(f"{integer_part}.{decimal_part}")

        start = point_index - len(first_number)
        #end = point_index + len(second_number)

        return make_result(value, line ,start, len(line))

    # тип "один и шесть" или "два целых пять"
    for word in ["и", "целых"]:
        if word in line:
            idx = line.index(word)
            if len(list_num) == 2:
                value = float(f"{int(list_num[0])}.{int(list_num[1])}")
                return make_result(value, line , idx - len(first_number), idx + len(list_num))

            elif len(list_num) > 2:
                value = list_num[0] + list_num[1] / list_num[2]
                return make_result(value, line ,idx - len(first_number), idx + len(list_num))

    # тип "пять десятых", "одна вторая"
    for i, word in enumerate(line):
        if word.endswith("ых") or word.endswith("ая"):

            if len(list_num) == 2:
                value = list_num[0] / list_num[1]
                return make_result(value, line, i - len(first_number), i + len(list_num))

            elif len(list_num) == 3:
                value = list_num[0] + list_num[1] / list_num[2]
                return make_result(value, line, i - len(first_number), i + len(list_num) + 1)

    return None


def get_half(list_num: list[int | float], line: list[str]) -> tuple[float, str] | None:
    try:
        number_in_string = str(list_num[0]) if list_num[0] % 10 != 0 else str(int(list_num[0] / 10))
    except IndexError:
        return None
    
    for i,word in enumerate(line):
        if word in half:
            if len(line) == 1:
                return make_result(half[word],line,i,i+1)
            return make_result(list_num[0] * half[word],line,i-len(number_in_string),i+1)

    return None


#---------------------------------------------------


def get_a_fraction_en(list_num: list[int | float], line:list[str]):
    if "point" not in line:
        return None

    string_assembly = ""
    for i in list_num:
        string_assembly += str(i)
    return string_assembly




def get_half_en(list_num: list[int | float], line: list[str]) -> tuple[float, str] | None:
    try:
        number_in_string = str(list_num[0]) if list_num[0] % 10 != 0 else str(int(list_num[0] / 10))
        for i,word in enumerate(line):
            if word in half_en:
                if len(line) == 1:
                    return make_result(half_en[word],line,i,i+1)
            
                return make_result(list_num[0] + half_en[word],line,i-len(number_in_string),i+1)
    except IndexError:  
        return None


# def get_a_part_en(list_num: list[int | float],line:list[str]):
#     if not list_num:
#         return None
    
#     for i in list_num:
#         if isinstance(i,float):
#             return -i if "minus" in line else i
    

def get_a_fraction_en(list_num: list[int | float], line:list[str]):
    if "point" not in line:
        return None
    
    first_number = str(list_num[0]) if list_num[0] % 10 != 0 else str(int(list_num[0] / 10))
    second_number = str(list_num[1]) if list_num[1] % 10 != 0 else str(int(list_num[1] / 10))

    for i,word in enumerate(line):
        if word == "point":
            string_assembly = f"{list_num[0]}.{list_num[1]}"
            return make_result(float(string_assembly),line,i-len(first_number),i+len(second_number) + 1)
    return None