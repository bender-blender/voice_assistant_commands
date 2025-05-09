from datetime import datetime
from stark import  Response
from dependencies import convert



class Data:
    """
    Date Query Class
    """

    def show_date(self):

        months = [
            'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
        ]

        data = datetime.now()
        day = data.day
        month = data.month
        year = data.year

        response_text = f"Сегодня {convert(day)} {months[month-1]} {convert(year)} года"

        return Response(voice=response_text)

