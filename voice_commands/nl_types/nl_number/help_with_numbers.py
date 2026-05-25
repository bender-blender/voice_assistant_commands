from .num_ru import fractions,half
from .num_en import half_en,part_en

import ru_word2number.w2n
from word2number.w2n import word_to_num


def make_result(value, line, start, end) -> tuple[float, str]:
    substring = " ".join(line[start:end])
    return value, substring

def get_part(list_num: list[int | float], line: list[str]) -> tuple[float,str] | None:
    check_fraction = [True if key in line else False for key in fractions.keys()]
    if not any(check_fraction):
        return None
    
    for i,word in enumerate(line):
        if word in fractions:
            if len(list_num) == 0:
                return make_result(fractions[word],line,i,i+1)
            
            number_in_string = str(list_num[0])
            calculation = list_num[0] * fractions[word]
            return make_result(calculation,line,i-len(number_in_string),i+1)



def get_a_fraction(list_num: list[int], line: list[str]) -> tuple[float,str] | None:
    if not list_num:
        return None

    first_number = str(list_num[0]) if list_num[0] % 10 != 0 else str(int(list_num[0] / 10))
    second_number = str(list_num[1]) if list_num[1] % 10 != 0 else str(int(list_num[1] / 10))
    # тип "три точка четырнадцать"
    if "точка" in line and len(list_num) >= 2:
        point_index = line.index("точка")

        integer_part = int(list_num[0])
        decimal_part = ''.join(str(int(x)) for x in list_num[1:])
        value = float(f"{integer_part}{decimal_part}")

        start = point_index - len(first_number)
        end = point_index + len(second_number)

        return make_result(value, line ,start, end)

    # тип "один и шесть" или "два целых пять"
    for word in ["и", "целых"]:
        if word in line:
            idx = line.index(word)
            if len(list_num) == 2:
                value = float(f"{int(list_num[0])}.{int(list_num[1])}")
                return make_result(value, line , idx - len(first_number), idx + len(second_number) + 1)

            elif len(list_num) > 2:
                value = list_num[0] + list_num[1] / list_num[2]
                return make_result(value, line ,idx - len(first_number), idx + len(second_number) + 2)

    # тип "пять десятых", "одна вторая"
    for i, word in enumerate(line):
        if word.endswith("ых") or word.endswith("ая"):

            if len(list_num) == 2:
                value = list_num[0] / list_num[1]
                return make_result(value, line, i - len(first_number), i + len(second_number))

            elif len(list_num) == 3:
                value = list_num[0] + list_num[1] / list_num[2]
                return make_result(value, line, i - len(first_number), i + len(second_number) + 1)

    return None


def get_half(list_num: list[int | float], line: list[str]) -> tuple[float, str] | None:
    check_half = [True if key in line else False for key in half.keys()]
    if not any(check_half):
        return None
    
    for i,word in enumerate(line):
        if word in half:
            string = " ".join(line)            
            if len(list_num) <= 1 or list_num[0] <= 1:
                return make_result(0.5,line,i,len(string))
        

            return make_result(list_num[0],line,i,len(string))

    return None


#---------------------------------------------------


def get_half_en(list_num:list[int | float] ,line: list[str]) -> tuple[float, str] | None:
    

    if "half" not in line:
        return None

    pharse_replace = " ".join(line).replace("-"," ")
    number = word_to_num(pharse_replace)
    inx_sub = []
    for i,word in enumerate(pharse_replace.split()):
        try:
           
            if word_to_num(word):
                inx_sub.append(i)
        except:
            if word == "half":
                inx_sub.append(i)
    
    if number <= 1:
        return make_result(0.5,line,inx_sub[0],inx_sub[-1] + 2) 
    return make_result(number+0.5,line,inx_sub[0],inx_sub[-1] + 2)


def get_a_part_en(list_num: list[int | float],line:list[str]):
    if not list_num:
        return None
    
    
    for i,num in enumerate(list_num):
        if isinstance(num,float):
            return make_result(num if "minus" not in line else -num,line,i,len(line))
            
    

def get_a_fraction_en(list_num: list[int | float], line:list[str]):
    if "point" not in line:
        return None
    first_number = str(list_num[0]) if list_num[0] % 10 != 0 else str(int(list_num[0] / 10))
    second_number = str(list_num[1]) if list_num[1] % 10 != 0 else str(int(list_num[1] / 10))

    for i,word in enumerate(line):
        if word == "point":
            string_assembly = f"{list_num[0]}{list_num[1]}"
            return make_result(float(string_assembly),line,i-len(first_number),i+len(second_number) + 1)
    return None