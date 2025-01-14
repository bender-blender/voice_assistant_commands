from num2words import num2words
def convert(number):  # Преобразовать число в строку
    word = num2words(number, lang="ru")
    return word