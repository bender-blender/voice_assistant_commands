from faker import Faker
from num2words import num2words
from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber
from random import randint,choice
import pytest


fake = Faker("ru_RU")

def create_pharse(number):
    text = fake.words(10)
    index = randint(0,len(text))
    text_number = num2words(number, lang='ru')
    
    
    split_pharse = text_number.split()
    if number < 0:
        split_pharse.insert(0,"минус")

    for word in split_pharse:
        text.insert(index,word)
        index += 1
    

    return " ".join(text)



@pytest.mark.asyncio
@pytest.mark.parametrize("_", range(10))
async def test_auto_number(_):
    options = [
        fake.random_int(0, 10000000),
        round(fake.random_int(10, 10000) / fake.random_int(10, 10000),2),
    ]

    number = choice(options)
    phrase = create_pharse(number)

    print(phrase)
    print(number)

    res = await pattern_parser.parse_object(NLNumber, phrase)
    assert res.obj.value == number
