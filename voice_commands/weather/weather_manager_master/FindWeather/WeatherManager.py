import json
import requests
import math
import datetime
from typing import List, Union, Tuple
import uuid
from .WeatherType import WeatherType
from .Current import Current
from .Day import Day



class WeatherManager:
    api_key: str
    location: Union[str, Tuple[float, float]]
    days_count: int

    def __init__(self, api_key: str, location: Union[str, Tuple[float, float]], days_count: int = 7):
        self.api_key = api_key
        self.location = location
        self.days_count = days_count

    def get_location_query(self) -> str:
        if isinstance(self.location, tuple) and len(self.location) == 2:
            lat, lon = self.location
            return f"{lat},{lon}"
        return self.location

    def get_url(self, function: str) -> str:
        base_url = 'api.weatherapi.com/v1'
        protocol = 'https'
        return f'{protocol}://{base_url}/{function}.json'

    def get_current(self) -> Union[Current, None]:
        params = {
            'key': self.api_key,
            'q': self.get_location_query()
        }
        response_info = requests.get(self.get_url('current'), params=params)

        if response_info.status_code != 200:
            print('Wrong URL or API error')
            return None

        try:
            data = response_info.json()
        except json.JSONDecodeError:
            print('Error decoding JSON')
            return None

        current = data.get('current', {})
        condition_dict = current.get('condition', {})
        code = condition_dict.get('code', 1000)

        return Current(
            cloud=current.get('cloud', 0.0),
            humidity=current.get('humidity', 0.0),
            temp_c=current.get('temp_c', 0.0),
            feels_like_c=current.get('feelslike_c', 0.0),
            wind_dir=current.get('wind_dir', ''),
            wind_kph=current.get('wind_kph', 0.0),
            pressure_in=current.get('pressure_in', 0.0),
            wind_degree_rad=(int(current.get('wind_degree', 0)) * math.pi / 180),
            weather_type=WeatherType.get_type_by_code(code),
            condition_text=condition_dict.get('text', ''),
            weather_condition=condition_dict.get('icon', '')
        )

    def get_days(self) -> List[Day]:
        params = {
            'key': self.api_key,
            'q': self.get_location_query(),
            'days': self.days_count
        }
        response_info = requests.get(self.get_url('forecast'), params=params)

        if response_info.status_code != 200:
            print('Wrong URL or API error')
            return []

        try:
            data = response_info.json()
        except json.JSONDecodeError:
            print('Error decoding JSON')
            return []

        forecast_days = data.get('forecast', {}).get('forecastday', [])
        days = []

        for day_data in forecast_days:
            date_str = day_data.get('date')
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')

            day_info = day_data.get('day', {})
            condition = day_info.get('condition', {})
            code = condition.get('code', 1000)

            day = Day(
                id=uuid.uuid4(),
                date=date_obj,
                cloud=day_info.get('cloud', 0.0),
                humidity=day_info.get('avghumidity', 0.0),
                temp_c=day_info.get('avgtemp_c', 0.0),
                feels_like_c=day_info.get('avgtemp_c', 0.0),
                wind_dir='',
                wind_kph=day_info.get('maxwind_kph', 0.0),
                pressure_in=day_info.get('pressure_in', 0.0),
                wind_degree_rad=0.0,
                weather_type=WeatherType.get_type_by_code(code),
                condition_text=condition.get('text', ''),
                weather_condition=condition.get('icon', ''),
                hours=[]
            )
            days.append(day)

        return days
