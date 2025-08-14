import asyncio

from stark import CommandsManager, Response

from voice_commands.apps.clock.timer.parameters.interval import Interval
from voice_commands.apps.clock.timer.providers.provider_timer import TimerProvider

timer = TimerProvider()
timer_manager = CommandsManager()


# type: ignore
@timer_manager.new(
    "(поставь|установи|запусти|заведи|включи|сделай|стартуй) (таймер|счётчик) (на|через) $interval:Interval"
)
async def call_timer(interval: Interval):
    response = timer.set_a_timer(interval)
    if isinstance(response, Response):
        # Если вернулся Response (ошибка), озвучиваем его
        yield response
    else:
        yield Response(voice="Таймер установлен")
        # Если вернулось число (секунды), ждём и уведомляем
        await asyncio.sleep(response)
        yield Response(voice="Таймер сработал!")


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
