from stark import CommandsManager, Response
import anyio
from dependencies.auxiliary_functions import convert


stopwatch_manager = CommandsManager()

class Stopwatch:
    def __init__(self):
        self.seconds = 0
        self.running = False
        stopwatch_manager.new(r"(включи|запусти) секундомер")(self.start)
        stopwatch_manager.new(r"(останови|выключи) секундомер")(self.stop)
        stopwatch_manager.new(r"сбросить секундомер")(self.reset)

    async def start(self):
        """Запускает секундомер"""
        if self.running:
            yield Response(voice="Секундомер уже работает!")
            return
        
        self.running = True
        yield Response(voice="Секундомер запущен...")

        while self.running:
            print(f"Прошло: {self.seconds} сек", end="\r")
            await anyio.sleep(1)
            self.seconds += 1

    async def stop(self):
        """Останавливает секундомер"""
        if not self.running:
            yield Response(voice="Секундомер уже остановлен!")
            return
        
        self.running = False
        yield Response(voice=f"\nСекундомер остановлен на {convert(self.seconds)}ой секунде")

    async def reset(self):
        """Сбрасывает секундомер"""
        if self.running:
            async for response in self.stop():
                yield response
        self.seconds = 0
        yield Response(voice="\nСекундомер сброшен.")