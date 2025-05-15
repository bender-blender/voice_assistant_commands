from stark import CommandsManager
from .example import Weather
from stark.core.types import String


weather_manager = CommandsManager()
weather = Weather()

@weather_manager.new("погода $time:String")
def call_weather_with_time(time:String):
    return weather.get_weather_with_time(time)


@weather_manager.new("погода")
def call_weather():
    return weather.get_weather()

@weather_manager.new("температура $time:String")
def call_temperatire_with_time(time:String):
    return weather.get_temperature_with_temperature(time)

@weather_manager.new("температура")
def call_temperatire_with_time():
    return weather.get_temperature()


@weather_manager.new("осадки $time:String")
def call_get_precipitation_with_temperature(time:String):
    return weather.get_precipitation_with_temperature(time)

@weather_manager.new("осадки")
def call_get_precipitation():
    return weather.get_precipitation()

@weather_manager.new("(особое|особые|уведомления|уведомление) $time:String")
def call_get_special_with_time(time:String):
    return weather.get_special_with_time(time)

@weather_manager.new("(особое|особые|уведомления|уведомление)")
def call_get_special():
    return weather.get_special()