from stark import CommandsManager
from .current_time import Time
from .current_date import Data
from .current_time_in_city import CityTime
from .stopwatch import Stopwatch
from stark.core.types import String

time_manager = CommandsManager()

data = Data()
time = Time()
city_time = CityTime()
stopwatch = Stopwatch()

@time_manager.new(r"(узнать|узнай|определить|определи|подскажи|уточни|сколько) время (в|для) (городе|города) $city:String")
def call_time_city(city:String):
    return city_time.get_time_in_city(city=city)

@time_manager.new("какое сегодня число|какая сегодня дата|какой сегодня день")
def call_data():
    return data.show_date()

@time_manager.new("(подскажи|скажи|сколько) время")
def call_time():
    return time.show_time()

@time_manager.new("(включи|запусти) секундомер")
def call_start_stopwatch():
    return stopwatch.start()

@time_manager.new("(останови|выключи) секундомер")
def call_stop_stopwatch():
    return stopwatch.stop()

@time_manager.new("сбросить секундомер")
def call_reset_stopwatch():
    return stopwatch.reset()