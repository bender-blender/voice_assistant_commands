import datetime

import dateparser
from num2words import num2words
from word2number import w2n
from translate import Translator


def num2word(number) -> str:  # Преобразовать число в строку
    word = num2words(number, lang="ru")
    return word


def word2num(word: str, lang: str) -> int  | float:
    translate = Translator(from_lang=lang,to_lang="en").translate(word)
    try:
        number = w2n.word_to_num(translate)
        return float(number)
    except ValueError:
        raise ValueError(f"Не удалось преобразовать слово '{word}' в число.")


# ---------------------------------


days_map = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "среду": 2,
    "четверг": 3,
    "пятница": 4,
    "пятницу": 4,
    "суббота": 5,
    "субботу": 5,
    "воскресенье": 6,
}


def parse_day_to_date(words: list) -> tuple[str,datetime.datetime] | None:
    list_date = [i for i in words if i in days_map]
    if len(list_date) == 0:
        return None

    find_value = list_date.copy()[0]

    target_weekday = days_map.get(find_value)

    today = datetime.date.today()
    today_weekday = today.weekday()
    if target_weekday is not None:
        if today_weekday <= target_weekday:
            days_ahead = target_weekday - today_weekday
        else:
            days_ahead = 7 - (today_weekday - target_weekday)
    else:
        return None
    next_date = today + datetime.timedelta(days=days_ahead)
    return (find_value, datetime.datetime.combine(next_date, datetime.time.min))


# ----------------------

dictionary_num = {
    "ноль": 0,
    "один": 1,
    "первого": 1,
    "первое": 1,
    "первый": 1,
    "два": 2,
    "две": 2,
    "второго": 2,
    "второе": 2,
    "второй": 2,
    "три": 3,
    "третий": 3,
    "третье": 3,
    "третьего": 3,
    "четыре": 4,
    "четвёртого": 4,
    "четвёртое": 4,
    "четвёртый": 4,
    "пять": 5,
    "пятого": 5,
    "пятое": 5,
    "пятый": 5,
    "шесть": 6,
    "шестого": 6,
    "шестое": 6,
    "шестой": 6,
    "семь": 7,
    "седьмого": 7,
    "седьмое": 7,
    "седьмой": 7,
    "восемь": 8,
    "восьмого": 8,
    "восьмое": 8,
    "восьмой": 8,
    "девять": 9,
    "девятого": 9,
    "девятое": 9,
    "девятый": 9,
    "десять": 10,
    "десятого": 10,
    "десятое": 10,
    "десятый": 10,
    "одиннадцать": 11,
    "одиннадцатого": 11,
    "одиннадцатое": 11,
    "одиннадцатый": 11,
    "двенадцать": 12,
    "двенадцатого": 12,
    "двенадцатое": 12,
    "двенадцатый": 12,
    "тринадцать": 13,
    "тринадцатого": 13,
    "тринадцатое": 13,
    "тринадцатый": 13,
    "четырнадцать": 14,
    "четырнадцатого": 14,
    "четырнадцатое": 14,
    "четырнадцатый": 14,
    "пятнадцать": 15,
    "пятнадцатого": 15,
    "пятнадцатое": 15,
    "пятнадцатый": 15,
    "шестнадцать": 16,
    "шестнадцатого": 16,
    "шестнадцатое": 16,
    "шестнадцатый": 16,
    "семнадцать": 17,
    "семнадцатого": 17,
    "семнадцатое": 17,
    "семнадцатый": 17,
    "восемнадцать": 18,
    "восемнадцатого": 18,
    "восемнадцатое": 18,
    "восемнадцатый": 18,
    "девятнадцать": 19,
    "девятнадцатого": 19,
    "девятнадцатое": 19,
    "девятнадцатый": 19,
    "двадцать": 20,
    "двадцатого": 20,
    "двадцатое": 20,
    "двадцатый": 20,
    "тридцать": 30,
    "тридцатого": 30,
    "тридцатое": 30,
    "тридцатый": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90,
    "сто": 100,
    "двести": 200,
    "триста": 300,
    "четыреста": 400,
    "пятьсот": 500,
    "шестьсот": 600,
    "семьсот": 700,
    "восемьсот": 800,
    "девятьсот": 900,
    "тысяча": 1000,
    "тысячи": 1000,
    "тысяче": 1000,
    "тысячу": 1000,
    "две тысячи": 2000,
    "двухтысячного": 2000,
    "двухтысячный": 2000,
}

months = [
    "январь",
    "января",
    "январе",
    "февраль",
    "февраля",
    "феврале",
    "март",
    "марта",
    "марте",
    "апрель",
    "апреля",
    "апреле",
    "май",
    "мая",
    "мае",
    "июнь",
    "июня",
    "июне",
    "июль",
    "июля",
    "июле",
    "август",
    "августа",
    "августе",
    "сентябрь",
    "сентября",
    "сентябре",
    "октябрь",
    "октября",
    "октябре",
    "ноябрь",
    "ноября",
    "ноябре",
    "декабрь",
    "декабря",
    "декабре",
]


def parse_day_phrase(words: list, dictionary=dictionary_num, list_month=months) -> tuple[str,datetime.datetime] | None:
    list_date = [i for i in words if i in dictionary]
    month = [i for i in words if i in list_month]
    
    if len(month) == 0 or len(list_date) == 0:
        return None
    
    else:

        list_copy = list_date.copy()
        for index, number in enumerate(list_date):
            if dictionary_num.get(number):
                list_date[index] = dictionary_num.get(number)
        list_with_numbers = [str(sum(list_date))]
        
        result = dateparser.parse(" ".join(list_with_numbers + month))
        if result is None:
            return None

        # Приводим к datetime
        if isinstance(result, datetime.date) and not isinstance(result, datetime.datetime):
            result = datetime.datetime.combine(result, datetime.time.min)

        now = datetime.datetime.now()
        if now > result:
            result = result.replace(year=result.year + 1)

        return (" ".join(list_copy + month), result)


# ----------------------

def parse_phrase_in_time(phrase:list) -> tuple[str,list[str]] | None:
    
    nums = [dictionary_num[i] for i in phrase if i in dictionary_num]
    returned_string = [i for i in phrase if i in dictionary_num]
    res:list[int] = []
    for n in nums:
        if res and res[-1] % 10 == 0 and n < 10:  
            res[-1] += n 
        else:
            res.append(n)
        
        
    for i in range(len(res) - 1, 0, -1):
        h, m = res[i-1], res[i]
        if h < 24 and m < 60:   
            return (f"{h}:{m}",returned_string)
    
    if len(res) == 1 and res[0] < 24: #! Если найдены только часы
        return (f"{res[0]}:*",returned_string)

    return None 