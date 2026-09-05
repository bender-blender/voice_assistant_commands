from abc import ABC
from typing import Optional

from pydantic import BaseModel

from .WeatherType import WeatherType


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
