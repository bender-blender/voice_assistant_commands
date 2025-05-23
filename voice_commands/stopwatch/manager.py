from .providers.provider_stopwatch import Stopwatch
from stark import CommandsManager, Response



stopwatch_manager = CommandsManager()

stopwatch = Stopwatch()

@stopwatch_manager.new("секундомер")
def call_start_stopwatch():
    stopwatch.start()
    return Response(voice="Секундомер запущен")

@stopwatch_manager.new("(сброс|сбросить)")
def call_elapsed_stopwatch():
    if stopwatch.start_time is None:
        return Response(voice="Секундомер не запущен")
    print(f"Секундомер остановлен: {stopwatch.elapsed()} с")
    