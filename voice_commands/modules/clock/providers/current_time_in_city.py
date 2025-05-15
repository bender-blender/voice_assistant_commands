from geopy.geocoders import Nominatim
from datetime import datetime
from stark import  Response
from stark.core.types import String
import pytz
from timezonefinder import TimezoneFinder
from dependencies.helpers import translate_city, convert

from dataclasses import dataclass


@dataclass
class CityTimeInfo: # Model
    city_name: str
    hour: str
    minute: str


class LocationProvider:
    
    def find(self, place: str) -> Location: # TODO: find out what is Location
        city_name = location.value.strip()

        geolocator = Nominatim(user_agent="city_time_app")

        if " " in city_name:
            city_name = city_name.replace(" ", "-")
        
        city_name = translate_city(city_name.title(),to_lang="en",from_lang="ru")
        print(city_name)
        
        # Получаем координаты города
        location = geolocator.geocode(city_name)
        
        return location

class CurrentTimeProvider: # Provider
    """current time in city X
    """

    def get_time(self, location: geocode | Location | None = None) -> datetime:
        # city_name = location.value.strip()

        # geolocator = Nominatim(user_agent="city_time_app")

        # if " " in city_name:
        #     city_name = city_name.replace(" ", "-")
        
        # city_name = translate_city(city_name.title(),to_lang="en",from_lang="ru")
        # print(city_name)
        
        # # Получаем координаты города
        # location = geolocator.geocode(city_name)
        # if not location:
        #     return Response(voice=f"Город {city_name} не найден.")
        
        # latitude = location.latitude
        # longitude = location.longitude
    
        # Ищем временную зону по координатам
        timezone_finder = TimezoneFinder()
        timezone_str = timezone_finder.timezone_at(
            lng=longitude, lat=latitude)
        
        if not timezone_str:
            return Response(voice=f"Не удалось определить временную зону для города {city_name}.")
        
        # Получаем текущее время в указанной временной зоне
        local_time = datetime.now(pytz.timezone(timezone_str))
        
        # hour = str(convert(local_time.hour))
        # minute = str(convert(local_time.minute))
        # print(hour,minute)
        # city_name = translate_city(city_name,"ru","en")
        return CityTimeInfo(city_name, local_time.hour, local_time.minute)
