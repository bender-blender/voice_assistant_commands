from .WeatherType import WeatherType

from abc import ABC


from pydantic import BaseModel


from uuid import UUID


from typing import Optional





class Info(ABC, BaseModel):


    weather_type: WeatherType


    cloud: float


    humidity: float


    temp_c: float


    feels_like_c: Optional[float]


    pressure_in: Optional[float]


    wind_dir: str


    wind_kph: float


    wind_degree_rad: float


    condition_text: str


    weather_condition: str