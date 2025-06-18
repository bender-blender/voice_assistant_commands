from stark import CommandsManager, Response
import datetime as dt
import dateparser
from stark.core.types import String
from ...helpers.helpers import day_to_date, parse_day_phrase
from .providers.provider_weather import WeatherProvider
from typing import Optional
from .parameters.location import Location
from ...providers.location_provider import LocationProvider
from ...parameters.time_interval import TimeInterval
from translate import Translator

def prepare_date(time_interval: Optional[TimeInterval | dt.datetime] = None) -> dt.datetime:
    if time_interval is None:
        return dt.datetime.now()

    if isinstance(time_interval, dt.datetime):
        return time_interval

    value = time_interval.value  # предполагается, что это строка
    parsed = day_to_date(value) or dateparser.parse(value) or parse_day_phrase(value)
    if parsed is None:
        raise Exception("Неверный формат даты")

    return parsed


weather_manager = CommandsManager()

weather = WeatherProvider()


@weather_manager.new("погода( $time_interval: TimeInterval)?( $coord:Location)?")
def call_weather(coord: Location | None = None, time_interval: TimeInterval | None = None):
    # Получаем координаты: если указаны — используем их, иначе — определяем по умолчанию
    location_coords = (
        LocationProvider().get_coordinates(str(coord.value))
        if coord else LocationProvider().get_coordinates()
    )

    time_phrase = time_interval.raw_input if time_interval else dt.datetime.now()


    date = prepare_date(time_phrase) # type: ignore

    weather_data = weather.get_data(location=location_coords)
    
    if not weather_data:
        return Response(voice="Не удалось получить данные о погоде.")

    if date.date() == weather_data.date.date():
        print(weather_data.condition_text)
        return Response(voice=f"{Translator(to_lang="ru",from_lang="en").translate(weather_data.condition_text)}")
    else:
        return Response(voice="Нет данных о погоде на указанную дату.")
