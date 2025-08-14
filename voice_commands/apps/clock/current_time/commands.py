from stark import CommandsManager, Response
from stark.core.types import String

from voice_commands.formatters.time import TimeFormatter
from voice_commands.providers.location_provider import LocationProvider

from ....helpers.helpers import num2word
from .providers.time_provider import TimeProvider

time_manager = CommandsManager()


@time_manager.new("время( $city:String)?")  # TODO: city:Location
def call_time(city: String | None = None):
    if city is not None:
        city_name = str(city.value).title()
    else:
        city_name = None

    coordinates = LocationProvider().get_coordinates(city_name)  # None будет обрабатываться внутри
    time = TimeProvider().get_time(coordinates)
    formatted_time = TimeFormatter(time).get_formatted_time()
    hour, minute = num2word(formatted_time[0]), num2word(formatted_time[1])

    if city is not None:
        sentence = f"В {city_name} сейчас {hour} часов {minute} минут"
    else:
        sentence = f"Сейчас {hour} часов {minute} минут"

    return Response(voice=sentence)


@time_manager.new("дата")
def call_date():
    now = TimeProvider().get_time()
    sentence = TimeFormatter(now).get_formatted_date()
    print(sentence)
    return Response(voice=sentence)
