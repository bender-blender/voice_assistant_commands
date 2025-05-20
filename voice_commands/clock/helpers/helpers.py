from num2words import num2words


def num2word(number) -> str:  # Преобразовать число в строку
    word = num2words(number, lang="ru")
    return word