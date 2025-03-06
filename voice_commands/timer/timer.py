from stark import CommandsManager, Response
from stark.core.types import String
import datetime
import dateparser
import asyncio
from dependencies import convert

timer_manager = CommandsManager()

def validate_time_format(interval_value: str):
    """Проверяет, что введённый формат времени валиден."""
    try:
        parsed_time = dateparser.parse(f"через {interval_value}")
        return parsed_time is not None
    except Exception:
        return False

class State:
    """
    timers status
    """

    def __init__(self):
        timer_manager.new("покажи таймер")(self.show_timer)
        timer_manager.new("проверить состояние таймера")(
            self.check_timer_status)
        timer_manager.new("(отмени|удали) (таймер|счётчик)")(self.cancel_timer)
        self.list_timer = []

    def show_timer(self):
        """Метод для получения списка активных таймеров"""
        if self.list_timer:
            active_timers = [
                f"Таймер {convert(index + 1)}" for index in range(len(self.list_timer))]
            return Response(voice=f"Активных таймеров: {convert(len(active_timers))}")
        else:
            return Response(voice="Нет активных таймеров.")
    
    def check_timer_status(self):
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


class Timer:
    """timer
    """
    state = State()

    def __init__(self):
        timer_manager.new("(поставь|установи|запусти|заведи|включи|сделай|стартуй)? (таймер|счётчик)? (на|через)? $interval:String")(
            self.set_a_timer)

    async def set_a_timer(self, interval: String):
        """Устанавливает таймер"""
        print(interval.value)
        start = datetime.datetime.now()
        end = dateparser.parse(f"{interval.value}", settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': start})
        # Проверка валидности формата времени
        if not validate_time_format(interval.value):
            yield Response(voice="Ошибка! Неправильный формат времени.")
            return

        # Вычисляем время окончания таймера
        if not end:
            yield Response(voice="Ошибка! Неправильный формат времени.")
            return

        # Проверка, что время не в прошлом
        delta = (end - start).total_seconds()
        if delta <= 0:
            yield Response(voice="Ошибка! Указано прошедшее время. Пожалуйста, установите правильный интервал.")
            return
        else:
            yield Response(voice=f"Таймер установлен на {interval.value}")
            self.state.list_timer.append(self)  # Добавляем таймер в список

        # Ждём завершения таймера
            await asyncio.sleep(delta)
        # Таймер завершён, удаляем его из списка
            self.state.list_timer.remove(self)
            yield Response(voice="Таймер завершен")