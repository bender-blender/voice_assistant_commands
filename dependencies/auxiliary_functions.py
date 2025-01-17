from num2words import num2words
from translate import Translator
def convert(number):  # Преобразовать число в строку
    word = num2words(number, lang="ru")
    return word

def translate_city(city:str, to_lang="en", from_lang="ru"):
    translator = Translator(to_lang=f"{to_lang}", from_lang=f"{from_lang}")
    translated_city = translator.translate(city)
    translated_city = translated_city.replace(" ", "_").title()
    return translated_city

class TimeInterval(object):
    """Интервал

    Args:
        object (_type_): _description_
    """
    word_to_number = {
    "ноль": 0,
    "один": 1, "одна": 1,
    "два": 2, "две": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90,
    "сто":100,
    "тысяча":1000
    }

    intervals_in_seconds = {
        "сек":1,
        "мин":60,
        "час":3600,
        "день":86400,
        "нед":604800,
    }


    def __init__(self,text: str):
        self.text = text #  Текст, куда будет попадать голос пользователя
        
    def text_to_number(self):
        words = self.text.lower().split() # Разбиваем строку на части
        result = 0
    
        for word in words:
            if word in self.word_to_number:
                result += self.word_to_number[word]
            for key in self.intervals_in_seconds.keys():
                if key in word :
                    result *= self.intervals_in_seconds[key]
                    yield result
        return result
