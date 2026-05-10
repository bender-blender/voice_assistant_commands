from stark.core.commands_context import CommandsContext
from utilits.gliner_processor import GliNERProcessor
from stark.core.parsing import RecognizedEntity
from typing import cast
import pytest



@pytest.fixture(scope="session")
def ner():
    return GliNERProcessor()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, obj",
    [
        ("Я живу в Киеве", ["киеве"]),
        ("Переехал в Харьков пару лет назад", ["харьков"]),
        ("Мы летим в Одессу завтра утром", ["одессу"]),
        ("Конференция проходила во Львове", ["львове"]),
        ("Он работает в Днепре", ["днепре"]),
        ("Переехал в Франкфурт на Одере пару лет назад",["франкфурт","одере"]),
        ("Вызови убер в Киев",["убер","киев"]),
        ("Какая погода в Сан Франциско",["сан франциско"]),
        ("Аэропорт Шереметьево далеко?", ["аэропорт шереметьево"]),
        ("Время в городе Париж",["париж"]),
        ("Подскажи где тут ближайший магазин АТБ",["атб"]),
        ("Путь к Сильпо",["сильпо"]),
        ("Где ближайший банкомат ПриватБанка", ["приватбанка"]),
        ("Построй маршрут к Макдональдсу", ["макдональдсу"]),
    ],
)
async def test_city_extraction(text: str, obj: list[str], ner:GliNERProcessor):
    recognized_entities: list[RecognizedEntity] = []
    await ner.process_string(text.lower(), cast(CommandsContext, None), recognized_entities)
    for i in recognized_entities:
        assert i.substring in obj