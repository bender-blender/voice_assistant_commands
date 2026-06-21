from stark.core.commands_context import CommandsContext
from utilits.gliner_processor import GliNERProcessor
from stark.core.parsing import RecognizedEntity
from stark.core.types.location import Location
from typing import cast
import pytest



@pytest.fixture(scope="session")
def ner():
    return GliNERProcessor()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, obj",
    [
        ("Я живу в Киеве", [Location("киеве")]),
        ("Переехал в Харьков пару лет назад", [Location("харьков")]),
        ("Мы летим в Одессу завтра утром", [Location("одессу")]),
        ("Конференция проходила во Львове", [Location("львове")]),
        ("Он работает в Днепре", [Location("днепре")]),
        ("Переехал в Франкфурт на Одере пару лет назад",[Location("франкфурт"),Location("одере")]),
        ("Вызови убер в Киев",[Location("убер"),Location("киев")]),
        ("Какая погода в Сан Франциско",[Location("сан франциско")]),
        ("Аэропорт Шереметьево далеко?", [Location("аэропорт шереметьево")]),
        ("Время в городе Париж",[Location("париж")]),
        ("Подскажи где тут ближайший магазин АТБ",[Location("атб")]),
        ("Путь к Сильпо",[Location("сильпо")]),
        ("Где ближайший банкомат ПриватБанка", [Location("приватбанка")]),
        ("Построй маршрут к Макдональдсу", [Location("макдональдсу")]),
    ],
)
async def test_city_extraction(text: str, obj: list[str], ner:GliNERProcessor):
    recognized_entities: list[RecognizedEntity] = []
    await ner.process_string(text.lower(), cast(CommandsContext, None), recognized_entities)
    

    lst = [Location(e.substring) for e in recognized_entities]
    assert lst == obj
    #assert recognized_entities == obj
    # for i in recognized_entities:
    #     assert i.substring in obj