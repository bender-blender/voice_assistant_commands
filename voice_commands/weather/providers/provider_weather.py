from ...helpers.helpers import day_to_date, parse_day_phrase
from ..weather_manager_master import WeatherManager
from ..custom_types.custom_city import CustomCity
from ...models.model_city import CityInfo
from stark.core.types import String
from dotenv import load_dotenv
from datetime import datetime
from stark import Response
import requests
import dateparser
import os




class WeatherProvider:
    
    def __init__(self):
        load_dotenv("examlpe.env")
        self.api_key = os.getenv("api_key")
        self.coord = None
    
    def define_the_place(self, location: CustomCity | None = None):
        
        if location is None:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            place = data.get("city", "Неизвестный город")
            self.coord = CityInfo(place).get_coordinates()
        else:
            self.coord =  CityInfo(location.terrain).get_coordinates()
        
        return self.coord
                    
    

    def prepare_data(self, time: String = None):
        if time is None:
            target_date = datetime.now()
            return target_date
        else:
            parsed = day_to_date(time.value)
            if parsed is None:
                parsed = dateparser.parse(time.value)
            if parsed is None:
                parsed = parse_day_phrase(time.value)
            if parsed is None:
                return Response(voice="Неверный формат")
            target_date = parsed
            return target_date


    def get_weather_parameters(self, time: String = None):
        if self.coord is None:
            self.define_the_place(None)

        target_date = self.prepare_data(time)
        

        weather = WeatherManager(api_key=self.api_key, location=self.coord, days_count=20)
        days = weather.get_days()
        return days, target_date

    
    def get_without_time(self):
        days, target_date = self.get_weather_parameters(None)
        if isinstance(target_date, Response):
            return target_date

    
        for day in days:
            if day.date.date() == target_date.date():
                return day
        return Response(voice="Нет данных о погоде на выбранную дату")

    
    def get_from_time(self, time: String):
        days, target_date = self.get_weather_parameters(time)
        if isinstance(target_date, Response):
            return target_date

        
        for day in days:
            if day.date.date() == target_date.date():
                return day
        return Response(voice="Нет данных о погоде на выбранную дату")
