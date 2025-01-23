from stark import Response, CommandsManager
import anyio
import time
stopwatch = CommandsManager()

elapsed_time = 0
running = False

@stopwatch.new('старт')
async def start_timer() -> Response:
    global running, elapsed_time
    if not running:
        running = True
        start_time = time.time()
        while running:
            elapsed_time = time.time() - start_time
            print(f"Прошло времени: {elapsed_time:.2f} секунд.", end='\r')
            await anyio.sleep(1)  # Асинхронная пауза на 1 секунду
    return Response(voice="Секундомер запущен.")

@stopwatch.new('(останови|выруби)')
async def stop_timer() -> Response:
    global running
    running = False
    return Response(voice=f"Секундомер остановлен. Прошло времени: {elapsed_time:.2f} секунд.")

@stopwatch.new('сброс')
async def reset_timer() -> Response:
    global elapsed_time, running
    elapsed_time = 0
    running = False
    return Response(voice="Секундомер сброшен.")

