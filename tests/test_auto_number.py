from faker import Faker
from num2words import num2words
from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_number.nl_number import NLNumber
from random import randint,choice
import pytest


fake = Faker("ru_RU")


def create_pharse(number):
    text = fake.sentence().split()
    index = randint(0,len(text))
    text_number = num2words(number, lang='ru')
    
    
    split_pharse = text_number.split()
    if number < 0:
        split_pharse.insert(0,"минус")

    for word in split_pharse:
        text.insert(index,word)
        index += 1
    

    return " ".join(text).replace("."," ").lower()


def generate_cases():
    cases = []
    for _ in range(1000):
        options = [
            fake.random_int(0, 10000000),
            round(fake.random_int(10, 10000) / fake.random_int(10, 10000), 3),
        ]
        number = choice(options)
        cases.append((create_pharse(number), number))
    return cases

cases = generate_cases()



@pytest.mark.parametrize("phrase,expected", cases)
@pytest.mark.asyncio
async def test_auto_number_integer(phrase, expected):
    res = await pattern_parser.parse_object(NLNumber, phrase)
    assert round(res.obj.value,2) == round(float(expected),2)