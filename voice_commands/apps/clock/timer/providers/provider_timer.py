from .....parameters.date_time import DateTime
from ..model.model_timer import TimerModel
from datetime import datetime
from stark import Response
from .....helpers.helpers import num2word

class TimerProvider:

    def __init__(self):
        self.list_timers = []

    def set_a_timer(self, interval: DateTime) -> int | Response:
        end_time = interval.value

        if end_time < datetime.now():
            return Response(voice="Указанное время уже прошло, пожалуйста, установите другое время.")

        seconds = TimerModel(end_time).return_seconds() # type: ignore
        self.list_timers.append(self)
        return seconds

    def get_a_list_of_timers(self) -> list | str:

        if self.list_timers:
            active_timers = [
                f"Таймер {num2word(index + 1)}" for index in range(len(self.list_timers))]
            return active_timers
        else:
            return "Нет активных таймеров."

    def check_timer_status(self) -> str:

        count = len(self.list_timers)
        if count:
            return f"Количество активных таймеров: {num2word(count)}"
        else:
            return "Нет активных таймеров."

    def cancel_timer(self):

        if not self.list_timers:
            return Response(voice="Нет таймеров для отмены.")

        self.list_timers.pop(0)
