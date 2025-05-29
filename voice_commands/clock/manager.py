from ..clock.timer.custom_types.custom_time_parser import CustomTimeParser
from .providers import TimeCommands,DateCommands,TimeCityProvider
from ..clock.timer.providers.provider_timer import TimerProvider
from ..helpers.helpers import num2word, numerals_dict
from stark import Response, CommandsManager
from stark.core.types import String
import asyncio


time_manager = CommandsManager()
time = TimeCommands()
date = DateCommands()
timer = TimerProvider()


@time_manager.new("время $city:String")
def call_time_in_city(city:String):
    result = TimeCityProvider(str(city.value).title()).get_time_by_coordinates().get_formatted_time().split(":")
    hour = num2word(int(result[0]))
    minute = num2word(int(result[1]))
    sentence = f"{hour} часов {minute} минут"
    return Response(voice=sentence)


@time_manager.new("время")
def call_time():
    result = time.get_time().get_formatted_time().split(":")
    hour = num2word(int(result[0]))
    minute = num2word(int(result[1]))
    sentence = f"{hour} часов {minute} минут"
    return Response(voice=sentence)


@time_manager.new("дата")
def call_date():
    result = date.get_date().get_formatted_date().split(" ")

    phrase = [num2word(int(i)) if i.isdigit() else i for i in result]
    phrase[0] = numerals_dict[result[0]]
    return Response(voice=f"Сегодня { ' '.join(phrase) }ого года")

@time_manager.new("(поставь|установи|запусти|заведи|включи|сделай|стартуй) (таймер|счётчик) (на|через) $interval:CustomTimeParser")
async def call_timer(interval:CustomTimeParser):
    response = timer.set_a_timer(interval)
    yield Response(voice=f"Таймер установлен")
    await asyncio.sleep(response)
    yield Response(voice=f"Таймер завершён")


@time_manager.new("покажи таймер")
def call_show_the_timer():
    response = timer.get_a_list_of_timers()
    if isinstance(response, list):
        return Response(voice=f"Активные таймеры: {', '.join(response)}")
    else:
        return Response(voice=response)

@time_manager.new("проверить состояние таймера")
def call_check_state_timer():
    response = timer.check_timer_status()
    return Response(voice=response)

@time_manager.new("(отмени|удали) (таймер|счётчик)")
def call_cancel_timer():
    response = timer.cancel_timer()
    if isinstance(response, Response):
        return response
    else:
        return Response(voice="Таймер отменён.")
