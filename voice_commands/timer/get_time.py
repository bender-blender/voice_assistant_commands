import anyio
from stark import Response, CommandsManager
from stark.core.types import String
from dependencies.auxiliary_functions import TimeInterval

timer = CommandsManager()

@timer.new(r'(Поставь|Установи|Запусти|Заведи|Включи|Сделай|Стартуй)? (таймер|счётчик)? (на|через)? $countdown:String')
async def set_timer(countdown: String):
    
    timer = TimeInterval(countdown.value).text_to_number()
    period = [i for i in timer]
    yield Response(voice=f"Таймер установлен на {countdown.value}")
    await anyio.sleep(period[-1])
    yield Response(voice=f"Таймер закончился")
