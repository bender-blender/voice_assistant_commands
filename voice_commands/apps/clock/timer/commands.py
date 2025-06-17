from voice_commands.apps.clock.timer.custom_types.custom_time_parser import CustomTimeParser
from voice_commands.apps.clock.timer.providers.provider_timer import TimerProvider
from stark import Response, CommandsManager
import asyncio


timer = TimerProvider()
timer_manager = CommandsManager()

@timer_manager.new("(поставь|установи|запусти|заведи|включи|сделай|стартуй) (таймер|счётчик) (на|через) $interval:CustomTimeParser") # type: ignore
async def call_timer(interval:CustomTimeParser):
    print(interval.value)
    response = timer.set_a_timer(interval)
    yield Response(voice=f"Таймер установлен")
    await asyncio.sleep(response) # type: ignore
    yield Response(voice=f"Таймер завершён")

@timer_manager.new("покажи таймер")
def call_show_the_timer():
    response = timer.get_a_list_of_timers()
    if isinstance(response, list):
        return Response(voice=f"Активные таймеры: {', '.join(response)}")
    else:
        return Response(voice=response)

@timer_manager.new("проверить состояние таймера")
def call_check_state_timer():
    response = timer.check_timer_status()
    return Response(voice=response)

@timer_manager.new("(отмени|удали) (таймер|счётчик)")
def call_cancel_timer():
    response = timer.cancel_timer()
    if isinstance(response, Response):
        return response
    else:
        return Response(voice="Таймер отменён.")
