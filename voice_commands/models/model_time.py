from datetime import datetime
import locale

class TimeModel:

    def __init__(self, target_datetime: datetime | None = None):
        self.current_date = target_datetime or datetime.now()
    
    def get_formatted_time(self) -> str:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        return self.current_date.strftime("%H:%M")
    
    def get_formatted_date(self) -> str:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        return self.current_date.strftime('%-d %B %Y')
