from .providers.provider_weather import WeatherProvider
from .custom_types.custom_city import CustomCity
from stark import Response, CommandsManager
from ..helpers.helpers import num2word
from geopy.geocoders import Nominatim
from stark.core.types import String
from translate import Translator


weather = WeatherProvider()
translator = Translator("ru","en")
weather_manager = CommandsManager()


# this is not needded

# @weather_manager.new("город $location:CustomCity")
# def define_city(location: CustomCity):
#     coordinates = LocationProvider().get_coordinates(location)
#     # geolocator = Nominatim(user_agent="geoapi")
#     # location = geolocator.reverse((place[0], place[1]), language="ru")

#     city = location.raw["address"].get("city") or \
#             location.raw["address"].get("town") or \
#             location.raw["address"].get("village") or \
#             location.raw["address"].get("hamlet")

#     return Response(voice=f"Город установлен: {city}")


# @weather_manager.new("город")
# def return_location():
#     place = weather.define_the_place(None)
#     geolocator = Nominatim(user_agent="geoapi")
#     location = geolocator.reverse((place[0], place[1]), language="ru")

#     city = location.raw["address"].get("city") or \
#             location.raw["address"].get("town") or \
#             location.raw["address"].get("village") or \
#             location.raw["address"].get("hamlet")


#     return Response(voice=f"Город установлен: {city}")


@weather_manager.new("погода $date:String") # TODO: parse date as a custom parameter
def call_weather(date: String | None):
    weather_info = weather.get_weather(date)
    condition = translator.translate(weather_info.condition_text)
    temperature = num2word(weather_info.temp_c) # TODO: return avg, min, and max (feels like) temp
    return Response(voice=f"{condition}, температура {temperature} градусов Цельсия")

@weather_manager.new("погода")
def call_weather_no_time():
    return call_weather(None)


# TODO:
    # instead of many separate commands for different parameters, return all of them (all primary) in one command
    # For example, "погода" should return all primary parameters like condition_text and temperature in one reponse.
    # Cherry-picking commands will be added later if needed, leave a TODO mark for that.


# @weather_manager.new("температура $time:String")
# def call_temperature(time: String):
#     response = weather.get_from_time(time)
#     if isinstance(response, Response):
#         return response
#     return Response(voice=f"{num2word(response.temp_c)} градусов")

# @weather_manager.new("температура")
# def call_temperature_no_time():
#     response = weather.get_without_time()
#     if isinstance(response, Response):
#         return response
#     return Response(voice=f"{num2word(response.temp_c)} градусов")

# @weather_manager.new("(особое|особые|уведомления|уведомление) $time:String")
# def call_special(time: String):
#     response = weather.get_from_time(time)
#     if isinstance(response, Response):
#         return response
#     return Response(voice=f"{translator.translate(response.weather_type)}")

# @weather_manager.new("(особое|особые|уведомления|уведомление)")
# def call_special_no_time():
#     response = weather.get_without_time()
#     if isinstance(response, Response):
#         return response
#     return Response(voice=f"{translator.translate(response.weather_type)}")

# @weather_manager.new("влажность $time:String")
# def call_humidity(time: String):
#     response = weather.get_from_time(time)
#     if isinstance(response, Response):
#         return response
#     return Response(voice=f"{num2word(round(response.humidity))} процентов")

# @weather_manager.new("влажность")
# def call_humidity_no_time():
#     response = weather.get_without_time()
#     if isinstance(response, Response):
#         return response
#     return Response(voice=f"{num2word(round(response.humidity))} процентов")
