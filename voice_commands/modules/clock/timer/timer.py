from stark import Response
from stark.core.types import String
import datetime
import dateparser
import asyncio
from dependencies import convert


@dataclass
class Timer:
    start: datetime
    stop: datetime
    
    @property
    def is_active(self) -> bool:
        """Проверяет, активен ли таймер"""
        return self.start < datetime.datetime.now() < self.stop
    
    @property
    def delta(self) -> int:
        """Вычисляет разницу между началом и концом таймера"""
        return (self.stop - self.start).total_seconds()
    
    @property
    def remaining_time(self) -> int:
        """Вычисляет оставшееся время таймера"""
        return (self.stop - datetime.datetime.now()).total_seconds()


Timer(start, stop).is_active # True or False

class TimerProvider:
                
    timers: list[Timer]

    def __init__(self):
        # self.list_timer = []
        self.timers = []
    
    @classmethod
    def validate_time_format(cls, interval_value: str):
        """Проверяет, что введённый формат времени валиден."""
        try:
            parsed_time = dateparser.parse(f"через {interval_value}")
            return parsed_time
        except Exception:
            return False

    async def set_a_timer(self, interval: String):
        """Устанавливает таймер"""
        start = datetime.datetime.now()
        end = dateparser.parse(f"{interval.value}", settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': start})
        # Проверка валидности формата времени
        if not self.validate_time_format(interval.value):
            yield Response(voice="Ошибка! Неправильный формат времени.")
            return

        # Вычисляем время окончания таймера
        if not end:
            yield Response(voice="Ошибка! Неправильный формат времени.")
            return

        # Проверка, что время не в прошлом
        if start > end:
            yield Response(voice="Ошибка! Указано прошедшее время. Пожалуйста, установите правильный интервал.")
            return
        else:
            yield Response(voice=f"Таймер установлен на {interval.value}")
            self.state.list_timer.append(self)  # Добавляем таймер в список

        # Ждём завершения таймера
            delta = (end - start).total_seconds()
            await asyncio.sleep(delta)
        # Таймер завершён, удаляем его из списка
            self.state.list_timer.remove(self)
            yield Response(voice="Таймер завершен")

    def get_timers_list(self) -> list[Timer]:
        """Метод для получения списка активных таймеров"""
        if self.list_timer:
            active_timers = [
                f"Таймер {convert(index + 1)}" for index in range(len(self.list_timer))]
            return Response(voice=f"Активных таймеров: {convert(len(active_timers))}")
        else:
            return Response(voice="Нет активных таймеров.")
    
    def check_timer_status(self) -> int: # seconds
        """Метод для проверки состояния всех активных таймеров"""
        if self.list_timer:
            return Response(voice="Все таймеры активны.")
        else:
            return Response(voice="Нет активных таймеров.")

    def cancel_timer(self):
        """Метод для отмены таймера"""
        if not self.list_timer:
            return Response(voice="Нет таймеров для отмены.")

        # В данном примере отмена будет осуществляться для первого таймера.
        timer_to_cancel = self.list_timer.pop(0)  # Удаляем первый таймер
        return Response(voice="Таймер отменён.")