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
    
    def define_the_city(self, location: CustomCity | None = None):

        if location is not None:
            print(location.terrain)
            self.coord = CityInfo(location.terrain).get_coordinates()
            
        else:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            city = data.get("city", "Неизвестный город")
            print(city)
            self.coord = CityInfo(city).get_coordinates()



    def return_location(self, location: CustomCity):
        return self.define_the_city(location)
    
    def find_a_city(self):
        return self.define_the_city(None)
    
    def __prepare_data(self, time: String | None = None):
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
            return target_date
        

    
    def get_any_parameter(self, time: String = None):
        
        target_date = self.__prepare_data(time)
        weather = WeatherManager(api_key=self.api_key, location=self.coord, days_count=20)
        days = weather.get_days()

        for day in days:
            if day.date.date() == target_date.date():
                return day

        return Response(voice="Нет данных о погоде на выбранную дату")

    
    def get_without_time(self):
        return self.get_any_parameter(None)
    
    def get_from_time(self, time: String):
        return self.get_any_parameter(time)

        