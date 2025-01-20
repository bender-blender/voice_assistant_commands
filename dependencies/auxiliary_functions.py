from num2words import num2words
def convert(number):  # Преобразовать число в строку
    word = num2words(number, lang="ru")
    return word



class TimeInterval:
    """Интервал времени, представленный в виде текста."""
    
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
        "сто": 100,
        "тысяча": 1000
    }

    intervals_in_seconds = {
        "секунда": 1, "секунд": 1, "сек": 1,
        "минута": 60, "минут": 60, "мин": 60,
        "час": 3600, "часов": 3600, "часа": 3600,
        "день": 86400, "дней": 86400, "дня": 86400,
        "неделя": 604800, "недель": 604800, "нед": 604800
    }

    def __init__(self, text: str):
        self.text = text.lower()  # Преобразуем текст в нижний регистр

    def text_to_number(self):
        words = self.text.split()  # Разбиваем строку на слова
        total_seconds = 0
        current_number = 0

        for word in words:
            if word in self.word_to_number:
                # Если слово - число, запоминаем его
                current_number = self.word_to_number[word]
            elif word in self.intervals_in_seconds:
                # Если слово - единица измерения времени, конвертируем
                total_seconds += current_number * self.intervals_in_seconds[word]
                current_number = 0  # Сбрасываем текущий номер

        return total_seconds
