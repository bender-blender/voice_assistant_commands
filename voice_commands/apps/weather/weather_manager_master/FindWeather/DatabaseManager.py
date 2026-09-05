from typing import List

from .Day import Day
from .DBModel import DBModel
from .Hour import Hour


class DatabaseManager:
    def __init__(self):
        self.days = None
        self.hours = None

    def create_database(self):
        self.days = DBModel(  # Сохраняем как атрибут класса
            "days",
            {
                "date": "text",
                "cloud": "real",
                "humidity": "real",
                "temp_c": "real",
                "feels_like_c": "real",
                "wind_dir": "text",
                "wind_kph": "real",
                "pressure_in": "real",
                "condition_text": "text",
                "weather_condition": "text",
                "day_id": "text",
            },
        )

        self.hours = DBModel(  # Сохраняем как атрибут класса
            "hours",
            {
                "hour_index": "integer",
                "cloud": "real",
                "humidity": "real",
                "temp_c": "real",
                "feels_like_c": "real",
                "wind_dir": "text",
                "wind_kph": "real",
                "pressure_in": "real",
                "wind_degree_rad": "real",
                "condition_text": "text",
                "weather_condition": "text",
                "day_id": "text",
            },
        )

    def save_days(self, days: List[Day]):
        if self.days is None:
            raise ValueError("Database not initialized. Call create_database() first.")

        for day in days:
            day_dict = {
                "date": day.date,
                "cloud": day.cloud,
                "humidity": day.humidity,
                "temp_c": day.temp_c,
                "feels_like_c": day.feels_like_c,
                "wind_dir": day.wind_dir,
                "wind_kph": day.wind_kph,
                "pressure_in": day.pressure_in,
                "condition_text": day.condition_text,
                "weather_condition": day.weather_condition,
                "day_id": str(day.id),
            }
            self.days.insert(day_dict)  # Теперь доступ есть

    def save_hours(self, hours: List[Hour]):
        if self.hours is None:
            raise ValueError("Database not initialized. Call create_database() first.")

        for hour in hours:
            hour_dict = {
                "hour_index": hour.hour_index,
                "cloud": hour.cloud,
                "humidity": hour.humidity,
                "temp_c": hour.temp_c,
                "feels_like_c": hour.feels_like_c,
                "wind_dir": hour.wind_dir,
                "wind_kph": hour.wind_kph,
                "pressure_in": hour.pressure_in,
                "wind_degree_rad": hour.wind_degree_rad,
                "condition_text": hour.condition_text,
                "weather_condition": hour.weather_condition,
                "day_id": str(hour.day_id),
            }
            self.hours.insert(hour_dict)  # Теперь доступ есть
