import pytest

from voice_commands.nl_types.nl_location.nl_location_implement import NLLocationImplement
from voice_commands.nl_types.nl_location.nl_location import NLLocation, NLLocationParse
from voice_commands.nl_types.parsing_context import pattern_parser



@pytest.fixture
def get_home():
    return NLLocationImplement("Жемчужная 3 Одесса")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, obj",
    [
        ("Я живу в Киеве", "киеве"),
        ("Переехал в Харьков пару лет назад", "харьков"),
        ("Мы летим в Одессу завтра утром", "одессу"),
        ("Конференция проходила во Львове", "львове"),
        ("Он работает в Днепре", "днепре"),
        ("Переехал в Франкфурт на Одере пару лет назад","франкфурт на одере"),
        ("Вызови убер в Киев","убер киев"),
        ("Какая погода в Сан Франциско","сан франциско"),
        ("Аэропорт Шереметьево далеко?", "аэропорт шереметьево"),
        ("Время в городе Париж","париж"),
        ("Подскажи где тут ближайший магазин АТБ","атб"),
        ("Путь к Сильпо","сильпо"),
        ("Где ближайший банкомат ПриватБанка", "приватбанка"),
        ("Построй маршрут к Макдональдсу", "макдональдсу"),
    ],
)

async def test_city_extraction(get_home, text: str, obj: str):
    home = get_home
    nl_location = NLLocation(None)
    nl_parse = NLLocationParse(pattern_parser,home.home)
    await nl_parse.did_parse(nl_location,text.lower())
    
    print(nl_location.loc_name, obj)
    
    assert nl_location.loc_name == obj
