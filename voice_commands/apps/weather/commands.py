from .providers.provider_weather import WeatherProvider
from voice_commands.helpers.helpers import num2word
from voice_commands.parameters import DateTime
from stark import CommandsManager, Response
from translate import Translator
from datetime import datetime


weather_manager = CommandsManager()
translate = Translator(to_lang="ru",from_lang="en")
weather = WeatherProvider()

@weather_manager.new("(погода|погоду)( $time:DateTime)?")
def call_weather(time: DateTime | None = None):

    forecast = weather.get_data()
    period = time.value if time and type(time.value) is datetime else datetime.now()
    data_for_forecast = []
    for day in forecast.get_days():
        if day.date.date() == period.date():
            data_for_forecast.append([day.temp_c,day.pressure_in,day.condition_text,day.humidity])

    *_,return_forecast = [parameter for parameter in data_for_forecast]
    return Response(
    text=(
        f"Температура: {return_forecast[0]} "
        f" Давление: {return_forecast[1]} "
        f" Тип: {translate.translate(return_forecast[2])}"
        f" Влажность: {return_forecast[3]}"
    ),
    voice=f"{translate.translate(return_forecast[2])} , {num2word(return_forecast[0])} градусов , Давление: {num2word(return_forecast[1])} , паскаль Влажность: {num2word(return_forecast[3])} процентов"
    )


#TODO Попытатся сделать прогноз на несколько частей суток