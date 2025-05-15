import locale
from datetime import datetime
from stark import  Response
from dependencies import convert


class STDate: # Model
    
    def __init__(self, target_datetime: datetime | None = None):
        self.current_date = target_datetime or datetime.now()

    def get_formatted_datetime(self) -> str:

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') # TODO: make env var 
        pretty_time = datetime(2024, 1, 5).strftime('Сегодня %-d %B %Y года')
        
        # TODO: numbers to words

        return pretty_time
    
    def get_formatted_time(self) -> str:

        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        pretty_time = datetime(2024, 1, 5).strftime('Сегодня %-d %B %Y года') # TODO: update template

        return pretty_time


# TODO: integrate Time into STDate

class Time:
    """time class."""
    
    
    def show_time(self):
        current_time = datetime.now()
        hours = current_time.hour
        minutes = current_time.minute
        
        response_text = f"Сейчас {convert(hours)} часов {convert(minutes)} минут"
        return Response(voice=response_text)


# import locale
# from datetime import datetime

# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# print(datetime(2024, 1, 5).strftime('Сегодня %-d %B %Y года'))

# google: python datetime string format
