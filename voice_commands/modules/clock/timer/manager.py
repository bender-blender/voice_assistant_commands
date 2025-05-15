from stark.core.types import String
from stark import CommandsManager
from .timer import State,Timer

timer_manager = CommandsManager()

state_timer = State()
timer = Timer(state=state_timer)

@timer_manager.new("(поставь|установи|запусти|заведи|включи|сделай|стартуй) (таймер|счётчик) (на|через) $interval:String")
def call_set_timer(interval: String):
    return timer.set_a_timer(interval)

@timer_manager.new("покажи таймер")
def call_show_the_timer():
    return state_timer.show_timer()

@timer_manager.new("проверить состояние таймера")
def call_check_state_timer():
    return state_timer.check_timer_status() # TODO: seconds to pretty time

@timer_manager.new("(отмени|удали) (таймер|счётчик)")
def call_cancel_timer():
    return state_timer.cancel_timer()


