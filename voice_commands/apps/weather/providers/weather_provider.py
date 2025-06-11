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

    def get_weather(self, date: String = None, location: Coordinates | None = None) -> Day:
        target_date = self._prepare_date(date) # TODO: this must be parsed in command; providers shouldn't parse or format anything directly

        weather = WeatherManager(api_key=self.api_key, location=location, days_count=20)

        for day in weather.get_days():
            if day.date.date() == target_date.date():
                return day

    # Private methods

    def _prepare_date(self, time: String = None) -> datetime: # TODO: what is time?
        # TODO: this must be parsed in command; providers shouldn't parse or format anything directly
        if time is None:
            return datetime.now()

        parsed = day_to_date(time.value)
        if parsed is None:
            parsed = dateparser.parse(time.value)
        if parsed is None:
            parsed = parse_day_phrase(time.value)
        if parsed is None:
            return Response(voice="Неверный формат") # TODO: no Response in providers; raise errors
        target_date = parsed
        return target_date

    # DUPLICATED METHODS
    #
    # def get_without_time(self):
    #     days, target_date = self.get_weather_parameters(None)

    #     if isinstance(target_date, Response):
    #         return target_date

    #     for day in days:
    #         if day.date.date() == target_date.date():
    #             return day

    #     return Response(voice="Нет данных о погоде на выбранную дату") # TODO: No Response in providers

    # def get_from_time(self, time: String): # get what?

    #     days, target_date = self.get_weather_parameters(time)

    #     if isinstance(target_date, Response):
    #         return target_date

    #     for day in days:
    #         if day.date.date() == target_date.date():
    #             return day

    #     return Response(voice="Нет данных о погоде на выбранную дату") # TODO: No Response in providers
