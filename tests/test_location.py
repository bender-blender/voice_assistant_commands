# import pytest
# from voice_commands.apps.weather.parameters.location import Location
# from stark.core.types import ParseError  



# @pytest.mark.asyncio
# @pytest.mark.parametrize("query, expected_city", [
#     ("Погода в городе Киев завтра", "Киев"),                      
#     ("Подскажи какая будет погода в Санкт Петербурге вечером",
#     "Санкт Петербурге"),  
#     ("Погода в Лондоне", "Лондоне"),                               
#     ("Какая погода в Париже", "Париже"),                           
# ])
# async def test_location_debug(query, expected_city, capsys):
#     param = Location(value=None)
#     result = await param.did_parse(query)

#     print("Результат парсинга:", result)

#     # Прочитать весь stdout/stderr после выполнения
#     captured = capsys.readouterr()

#     print("=====================")
#     print(captured.out)   # всё, что было напечатано в stdout
#     print(captured.err)   # stderr (если был)
#     print("=====================")
#     assert expected_city in result


# @pytest.mark.asyncio
# @pytest.mark.parametrize("query", [
#     "Просто поговорим",
#     "ничего не понятно",
#     "расскажи что-нибудь интересное",
# ])
# async def test_location_fail(query):
#     parameter = Location(value=None)

#     with pytest.raises(ParseError):
#         await parameter.did_parse(query)



