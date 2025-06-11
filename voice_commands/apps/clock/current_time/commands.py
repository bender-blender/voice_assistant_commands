from ..clock.timer.custom_types.custom_time_parser import CustomTimeParser
from .providers import TimeCommands,DateCommands,TimeProvider
from ..clock.timer.providers.provider_timer import TimerProvider
from ..helpers.helpers import num2word, numerals_dict
from stark import Response, CommandsManager
from stark.core.types import String
import asyncio
from voice_commands.providers.location_provider import LocationProvider
from voice_commands.formatters.time import TimeFormatter


time_manager = CommandsManager()

@time_manager.new("время в $city:String") # TODO: city:Location
def call_time_in_city(city: String):
    coordinates = LocationProvider().get_coordinates(str(city.value).title())
    time = TimeProvider().get_time(coordinates)
    formatted_time = TimeFormatter(time).get_formatted_time()
    sentence = f"В {city} сейчас {formatted_time}"
    return Response(voice=sentence)

@time_manager.new("время")
def call_time():
    now = TimeProvider().get_time()
    sentence = TimeFormatter(now).get_formatted_time()
    return Response(voice=sentence)

@time_manager.new("дата")
def call_date():
    now = TimeProvider().get_time()
    sentence = TimeFormatter(now).get_formatted_date()
    return Response(voice=sentence)
