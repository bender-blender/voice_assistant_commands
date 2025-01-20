from dependencies.auxiliary_functions import convert
from stark.core.types import String
from stark import Response, CommandsManager
import datetime
import pytz 
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
time_city = CommandsManager()

@time_city.new(r"(сколько|какое|узнать|узнай|определить|определи|подскажи) время (в|для) (городе|города)? $city:String")
def get_current_time_in_city(city:String):
    city_name = f"{city.value}"

    # Создаем объект геокодера
    geolocator = Nominatim(user_agent="city_time_app")
    if " " in city_name:
        city_name = city_name.replace(" ","-")
    # Получаем координаты города
    location = geolocator.geocode(city_name)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        
        # Ищем временную зону по координатам
        timezone_finder = TimezoneFinder()
        timezone_str = timezone_finder.timezone_at(lng=longitude, lat=latitude)
        
        if timezone_str:
            # Получаем текущее время в указанной временной зоне
            local_time = datetime.datetime.now(pytz.timezone(timezone_str))
            hour  = convert(local_time.hour)
            minute = convert(local_time.minute)
            # Форматируем вывод
            return Response(voice=f"Текущее время в {city_name}: {hour} часов {minute} минут")
        else:
            return Response(voice=f"Не удалось определить временную зону для города {city_name}")
    else:
        return Response(voice=f"Город {city_name} не найден")