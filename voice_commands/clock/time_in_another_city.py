from dependencies.auxiliary_functions import convert, translate_city
from stark.core.types import String
from stark import Response, CommandsManager
import datetime
import pytz 

time_city = CommandsManager()

@time_city.new(r"(сколько|какое|узнать|узнай|определить|определи|подскажи) время (в|для) (городе|города) $city:String")
def get_time_in_city(city: String) -> Response:
    """
    Определение времени в указанном городе.
    """
    city_name = city.value
    #Переводим название города с русского на английский
    translated_city = translate_city(city=city_name).title()
    
    # Поиск временной зоны
    for timezone in pytz.all_timezones:
       # Проверяем, совпадает ли название города с одной из частей временной зоны
        if translated_city in timezone.replace(" ", "_").split('/') or translated_city in timezone.replace("-", "_").split('/'):
            # Если найдено совпадение, возвращаем текущее время
            tz = pytz.timezone(timezone)
            city_time = datetime.datetime.now(tz)
            hour = convert(city_time.hour)
            minute = convert(city_time.minute)
            translated_city = translate_city(city_name,to_lang="ru",from_lang="en")
            return Response(voice=f"Время в городе {translated_city} {hour} часов {minute} минут")
    return Response(voice="Не удалось распознать город")