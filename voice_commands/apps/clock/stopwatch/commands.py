from stark import CommandsManager, Response

from .providers.stopwatch_provider import StopwatchProvider

stopwatch_manager = CommandsManager()
stopwatch = StopwatchProvider()


@stopwatch_manager.new("проверь секундомер")
def elapsed():
    if stopwatch.start_time is None:
        return Response(voice="Секундомер не запущен")
    
    print(f"Прошло: {stopwatch.elapsed()} секунд")  # TODO: convert to time interval and format it nicely
    

@stopwatch_manager.new("секундомер")
def start():
    stopwatch.start()
    return Response(voice="Секундомер запущен")


@stopwatch_manager.new("(сброс|сбросить)")
def stop():
    if stopwatch.start_time is None:
        return Response(voice="Секундомер не запущен")

    print(f"Секундомер остановлен: {stopwatch.elapsed()} с") 
    stopwatch.reset()


