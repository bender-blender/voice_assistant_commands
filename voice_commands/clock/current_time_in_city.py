from geopy.geocoders import Nominatim
from datetime import datetime
from stark import  Response
from stark.core.types import String
import pytz
from timezonefinder import TimezoneFinder
from dependencies.auxiliary_functions import translate_city, convert



class CityTime:
    """current time in city X
    """

    def get_time_in_city(self, city: String):
        city_name = city.value.strip()

        geolocator = Nominatim(user_agent="city_time_app")

        if " " in city_name:
            city_name = city_name.replace(" ", "-")
        
        city_name = translate_city(city_name.title(),to_lang="en",from_lang="ru")
        print(city_name)
        
        # Получаем координаты города
        location = geolocator.geocode(city_name)
        if location:
            latitude = location.latitude
            longitude = location.longitude
        # Ищем временную зону по координатам
            timezone_finder = TimezoneFinder()
            timezone_str = timezone_finder.timezone_at(
                lng=longitude, lat=latitude)
            
            if timezone_str:
                # Получаем текущее время в указанной временной зоне
                local_time = datetime.now(pytz.timezone(timezone_str))
                hour = str(convert(local_time.hour))
                minute = str(convert(local_time.minute))
                print(hour,minute)
                city_name = translate_city(city_name,"ru","en")
                return Response(voice=f"Текущее время в городе {city_name}: {hour} часов {minute} минут.")
            else:
                return Response(voice=f"Не удалось определить временную зону для города {city_name}.")
        else:
            return Response(voice=f"Город {city_name} не найден.")
