from .current_time.commands import manager as ctime_manager
from .timer.commands import manager as timer_manager
from .stopwatch.commands import manager as stopwatch_manager

manager = CommandsManager()
manager.extend(ctime_manager)
manager.extend(timer_manager)
manager.extend(stopwatch_manager)
