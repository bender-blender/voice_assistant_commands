from stark import Response, CommandsManager
import anyio


stopwatch = CommandsManager()
STATE = True
@stopwatch.new(r"активируй секундомер")
async def start():    
    global STATE  # Указываем, что используем глобальную переменную STATE
    time = 0
    yield Response(voice="Засекла секундомер")
    while True:
        await anyio.sleep(1)
        time += 1
        if not STATE:  # Проверяем состояние глобальной переменной
            print(f"Работал {time} секунд")
            STATE = True  # Сбрасываем состояние для следующего использования
            yield Response(voice="Секундомер выключен")
            break

@stopwatch.new(r"(заверши|выруби|останови) секундомер")
async def stop():
    global STATE
    STATE = False


