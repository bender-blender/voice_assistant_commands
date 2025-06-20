from ...helpers.helpers import day_to_date, parse_day_phrase, num2word
from ...providers.location_provider import LocationProvider
from .providers.provider_weather import WeatherProvider
from ...parameters.time_interval import TimeInterval
from stark import CommandsManager, Response
from .parameters.location import Location
from stark.core import ResponseHandler
from translate import Translator
import datetime as dt
import dateparser


weather_manager = CommandsManager()

weather = WeatherProvider()


@weather_manager.new("погода")
def call_weather():
    return Response(voice="Где?", commands=[get_city_name])


@weather_manager.new("$coord:Location", hidden=True)
def get_city_name(coord: Location):
    return Response(
        voice="Когда?",
        commands=[get_the_weather],
        parameters={"coord": coord.value}
    )


@weather_manager.new("$time_interval:TimeInterval", hidden=True)
def get_the_weather(time_interval: TimeInterval, handler: ResponseHandler, **params):

    coord = params.get("coord")
    coord = LocationProvider().get_coordinates(coord)

    if coord is None:
        return Response(voice="Не удалось определить координаты. Попробуйте ещё раз.")
    
    print(f"Координаты:{coord}")

    value = time_interval.value

    if isinstance(value, dt.datetime):
        parsed = value
    else:
        parsed = day_to_date(value) or dateparser.parse(value) or parse_day_phrase(value)
        if parsed is None:
            raise Exception("Неверный формат даты")

    weather_data = weather.get_data(location=coord)
    translate = Translator(from_lang="en", to_lang="ru")

    for day in weather_data.get_days():
        if day.date.date() == parsed.date():
            return Response(voice=f"{translate.translate(day.condition_text)}, {num2word(day.temp_c)} градусов, {num2word(int(day.humidity))} милиметров осадков, {translate.translate(day.weather_type)}")
    handler.pop_context()
