from ..weather_manager_master import WeatherManager
from ....providers.location_provider import Coordinates
from dotenv import load_dotenv
import os


class WeatherProvider:

    def __init__(self):
        load_dotenv("example.env")
        self.api_key = os.getenv("api_key")

    def get_data(self, location: Coordinates | None = None) -> WeatherManager: # type: ignore

        weather = WeatherManager(api_key=self.api_key, location=location, days_count=10) # type: ignore
        return weather
