from .providers.provider_weather import WeatherProvider
from stark import Response, CommandsManager
from stark.core.types import String
from .custom_types.custom_city import CustomCity
from ..helpers.helpers import num2word
from translate import Translator


weather = WeatherProvider()
translate = Translator("en","ru")
weather_manager = CommandsManager()

@weather_manager.new("город $location:CustomCity")
def define_city(location: CustomCity):
    weather.return_location(location)
    return Response(voice=f"Город установлен: {location.terrain}")

@weather_manager.new("город")
def return_location():
    city = weather.find_a_city()
    return Response(voice=f"Город: {city}")


@weather_manager.new("погода $time:String")
def call_weather(time: String):
    response = weather.get_any_parameter(time)
    if isinstance(response, Response):
        return response
    return Response(voice=f"{translate.translate(response.condition_text)}")

@weather_manager.new("погода")
def call_weather_no_time():
    response = weather.get_any_parameter()
    if isinstance(response, Response):
        return response
    return Response(voice=f"{translate.translate(response.condition_text)}")


@weather_manager.new("температура $time:String")
def call_temperature(time: String):
    response = weather.get_any_parameter(time)
    return Response(voice=f"{num2word(response.temp_c)} градусов")

@weather_manager.new("температура")
def call_temperature_no_time():
    response = weather.get_any_parameter()
    return Response(voice=f"{num2word(response.temp_c)} градусов")

@weather_manager.new("(особое|особые|уведомления|уведомление) $time:String")
def call_special(time: String):
    response = weather.get_any_parameter(time)
    return Response(voice=f"{translate.translate(response.weather_type)}")

@weather_manager.new("(особое|особые|уведомления|уведомление)")
def call_special_no_time():
    response = weather.get_any_parameter()
    if isinstance(response, Response):
        return response
    return Response(voice=f"{translate.translate(response.weather_type)}")

@weather_manager.new("влажность $time:String")
def call_humidity(time: String):
    response = weather.get_any_parameter(time)
    if isinstance(response, Response):
        return response
    return Response(voice=f"{num2word(round(response.humidity))} процентов")

@weather_manager.new("влажность")
def call_humidity_no_time():
    response = weather.get_any_parameter()
    if isinstance(response, Response):
        return response
    return Response(voice=f"{num2word(round(response.humidity))} процентов")