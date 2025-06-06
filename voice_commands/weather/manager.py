from .providers.provider_weather import WeatherProvider
from .custom_types.custom_city import CustomCity
from stark import Response, CommandsManager
from ..helpers.helpers import num2word
from geopy.geocoders import Nominatim
from stark.core.types import String
from translate import Translator


weather = WeatherProvider()
translate = Translator("ru","en") 
weather_manager = CommandsManager()


@weather_manager.new("город $location:CustomCity")
def define_city(location: CustomCity):
    place = weather.define_the_place(location)
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.reverse((place[0], place[1]), language="ru")

    city = location.raw["address"].get("city") or \
            location.raw["address"].get("town") or \
            location.raw["address"].get("village") or \
            location.raw["address"].get("hamlet")
    
    
    return Response(voice=f"Город установлен: {city}")


@weather_manager.new("город")
def return_location():
    place = weather.define_the_place(None)
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.reverse((place[0], place[1]), language="ru")

    city = location.raw["address"].get("city") or \
            location.raw["address"].get("town") or \
            location.raw["address"].get("village") or \
            location.raw["address"].get("hamlet")
    
    
    return Response(voice=f"Город установлен: {city}")


@weather_manager.new("погода $time:String")
def call_weather(time: String):
    response = weather.get_from_time(time)
    if isinstance(response, Response):
        return response
    return Response(voice=f"{translate.translate(response.condition_text)}")

@weather_manager.new("погода")
def call_weather_no_time():
    response = weather.get_without_time()
    if isinstance(response, Response):
        return response
    return Response(voice=f"{translate.translate(response.condition_text)}")


@weather_manager.new("температура $time:String")
def call_temperature(time: String):
    response = weather.get_from_time(time)
    if isinstance(response, Response):
        return response
    return Response(voice=f"{num2word(response.temp_c)} градусов")

@weather_manager.new("температура")
def call_temperature_no_time():
    response = weather.get_without_time()
    if isinstance(response, Response):
        return response
    return Response(voice=f"{num2word(response.temp_c)} градусов")

@weather_manager.new("(особое|особые|уведомления|уведомление) $time:String")
def call_special(time: String):
    response = weather.get_from_time(time)
    if isinstance(response, Response):
        return response
    return Response(voice=f"{translate.translate(response.weather_type)}")

@weather_manager.new("(особое|особые|уведомления|уведомление)")
def call_special_no_time():
    response = weather.get_without_time()
    if isinstance(response, Response):
        return response
    return Response(voice=f"{translate.translate(response.weather_type)}")

@weather_manager.new("влажность $time:String")
def call_humidity(time: String):
    response = weather.get_from_time(time)
    if isinstance(response, Response):
        return response
    return Response(voice=f"{num2word(round(response.humidity))} процентов")

@weather_manager.new("влажность")
def call_humidity_no_time():
    response = weather.get_without_time()
    if isinstance(response, Response):
        return response
    return Response(voice=f"{num2word(round(response.humidity))} процентов")