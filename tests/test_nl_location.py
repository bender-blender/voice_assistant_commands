import pytest
from voice_commands.nl_types.nl_location.nl_location import NLLocation



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text, obj",
    [
        ("Киев", "киев"),
        ("Харьков", "харьков"),
        ("Одесса", "одесса"),
        ("Львов", "львов"),
        ("Днепр", "днепр"),
        ("Франкфурт","франкфурт"),
        ("убер","убер"),
        ("аэропорт шереметьево", "аэропорт шереметьево"),
        ("АТБ","атб"),
        ("Сильпо","сильпо"),
        ("ПриватБанк", "приватбанк"),
        ("Макдональдс", "макдональдс"),
    ],
)
async def test_city_extraction(text: str, obj: str):
    nl_location = NLLocation(None)
    
    await nl_location.did_parse(text.lower()) 
    assert type(nl_location.places) is dict
    assert nl_location.value == obj

# e2e tests:
# https://github.com/MarkParker5/STARK/blob/master/tests/test_commands_flow/test_command_run.py
# https://github.com/MarkParker5/STARK/blob/0113017e02218434733c068bca36ca91fcc80b1a/tests/conftest.py#L69
