from dependencies.helpers import convert, day_to_date, parse_day_phrase
from .weather_manager_master import WeatherManager
from stark.core.types import String
from translate import Translator
from datetime import datetime
from stark import Response
import dateparser
import requests


class Weather:
    """Класс погода
    """

    def __init__(self):
        self.city = self.set_up_city()
        self.translate = Translator(to_lang="ru", from_lang="en")
        self.api_key = "6529245dc1ac4297849161313250105"
    

    @classmethod
    def set_up_city(cls):
        """Определить город пользователя по IP"""
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        # Если город не найден, вернуть "Неизвестный город"
        return data.get("city", "Неизвестный город")

    def prepare_data(self, time: String = None):
        """Подготовить данные к дальнейшей работе с Api
        """
        if time is None:
            target_date = datetime.now()
        else:
            parsed = day_to_date(time.value)
            if parsed is None:
                parsed = dateparser.parse(time.value)
            if parsed is None:
                parsed = parse_day_phrase(time.value)
            if parsed is None:
                return Response(voice="Неверный формат")
            target_date = parsed

        weather = WeatherManager(api_key=self.api_key, place_code=self.city, days_count=20)
        days = weather.get_days()

        for day in days:
            if day.date.date() == target_date.date():
                return day

        return Response(voice="Нет данных о погоде на указанную дату")

    
    def weather(self, time: String = None):
        """Погода"""
        day = self.prepare_data(time)
        if isinstance(day, Response):
            return day
    
        return Response(voice=f"{self.translate.translate(day.condition_text)}")

    def temperature(self, time: String = None):
        """Температура
        """
        day = self.prepare_data(time)
    
        if isinstance(day, Response):
            return day
    
        return Response(voice=f"{convert(day.temp_c)} градуса")

    def special(self, time: String = None):
        """
        Особые уведомление
        """
        day = self.prepare_data(time)
        if isinstance(day, Response):
            return day
    
        return Response(voice=f"{day.weather_type}")



    def precipitation(self, time: String = None):
        day = self.prepare_data(time)
        if isinstance(day, Response):
            return day
    
        return Response(voice=f"{convert(round(day.humidity))} процентов")
        

    def get_weather(self):
        return self.weather()

    def get_weather_with_time(self, time: String):
        return self.weather(time)
    
    def get_temperature(self):
        return self.temperature()
    
    def get_temperature_with_temperature(self, time: String):
        return self.temperature(time)
    
    def get_special(self):
        return self.special()
    
    def get_special_with_time(self, time: String):
        return self.special(time)
    
    def get_precipitation(self):
        return self.precipitation()
    
    def get_precipitation_with_temperature(self, time: String):
        return self.precipitation(time)
    
