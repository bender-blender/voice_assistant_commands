import os
from dotenv import load_dotenv
from ..weather_manager_master.FindWeather.WeatherManager import WeatherManager
from voice_commands.providers.location_provider import LocationProvider

class WeatherProvider:
    """
    """
    def __init__(self):
        load_dotenv("example.env")
        self.api_key = os.getenv("api_key")
        self.location = LocationProvider().get_coordinates()

    def get_data(self) -> WeatherManager:
        weather = WeatherManager(api_key=self.api_key, location=self.location, days_count=10)  # type: ignore
        return weather
