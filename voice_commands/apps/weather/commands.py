from ...helpers.helpers import  num2word
from .providers.provider_weather import WeatherProvider
from ...parameters.date_time import DateTime
from stark import CommandsManager, Response
from .parameters.location import Location
from stark.core import ResponseHandler
from translate import Translator
import dateparser


weather_manager = CommandsManager()

weather = WeatherProvider()



@weather_manager.new("погода( $time:DateTime)?( $location:Location)?")
def call_weather(time:DateTime | None = None, location: Location | None = None):
    print(time.value)
    print(location.coord)
    



# @weather_manager.new("$time_interval:TimeInterval", hidden=True)
# def get_the_weather(time_interval: DateTime, handler: ResponseHandler, location:Location):

#     coord = LocationProvider().get_coordinates(location.value)

#     if coord is None:
#         return Response(voice="Не удалось определить координаты. Попробуйте ещё раз.")
    
#     print(f"Координаты:{coord}")

#     value = time_interval.value

    
#     parsed = day_to_date(value) or dateparser.parse(value) or parse_day_phrase(value)
#     if parsed is None:
#         raise Exception("Invalid date format")

#     weather_data = weather.get_data(location=coord)
#     translate = Translator(from_lang="en", to_lang="ru")

#     for day in weather_data.get_days():
#         if day.date.date() == parsed.date():
#             return Response(voice=f"{translate.translate(day.condition_text)}, {num2word(day.temp_c)} градусов, {num2word(int(day.humidity))} милиметров осадков, {translate.translate(day.weather_type)}")
#     handler.pop_context()
