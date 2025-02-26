from datetime import datetime
from stark import CommandsManager, Response
from dependencies.auxiliary_functions import convert

data_manager = CommandsManager()


class Data:
    """
    Date Query Class
    """

    def __init__(self):
        data_manager.new(
            "(какое сегодня число|какая сегодня дата|какой сегодня день)")(self.show_date)

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

        # print("Сгенерированный ответ с датой:", response_text)

        return Response(voice=response_text)
