from stark import Response, CommandsManager
from .providers import TimeCommands,DateCommands,TimeCityProvider
from .helpers.helpers import num2word, numerals_dict
from stark.core.types import String


time_manager = CommandsManager()
time = TimeCommands()
date = DateCommands()


@time_manager.new("время $city:String")
def call_time_in_city(city:String):
    result = TimeCityProvider(str(city.value).title()).get_time_by_coordinates().get_formatted_time().split(":")
    hour = num2word(int(result[0]))
    minute = num2word(int(result[1]))
    sentence = f"{hour} часов {minute} минут"
    return Response(voice=sentence)


@time_manager.new("время")
def call_time():
    result = time.get_time().get_formatted_time().split(":")
    hour = num2word(int(result[0]))
    minute = num2word(int(result[1]))
    sentence = f"{hour} часов {minute} минут"
    return Response(voice=sentence)


@time_manager.new("дата")
def call_date():
    result = date.get_date().get_formatted_date().split(" ")

    phrase = [num2word(int(i)) if i.isdigit() else i for i in result]
    phrase[0] = numerals_dict[result[0]]
    return Response(voice=f"Сегодня { ' '.join(phrase) }ого года")
    