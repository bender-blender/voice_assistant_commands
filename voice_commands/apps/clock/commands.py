from stark import CommandsManager

from .current_time.commands import time_manager
from .stopwatch.commands import stopwatch_manager
from .timer.commands import timer_manager
from .alarm.commands import alarm_manager

manager = CommandsManager()
manager.extend(time_manager)
manager.extend(stopwatch_manager)
manager.extend(timer_manager)
manager.extend(alarm_manager)
