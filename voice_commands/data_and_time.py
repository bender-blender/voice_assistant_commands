from dependencies.auxiliary_functions import convert
from stark import CommandsManager, Response
from datetime import datetime

manager = CommandsManager()

@manager.new("(назови дату|сегодняшняя дата)?")
def get_the_day() -> Response:
    today = datetime.now()  
    day = today.day         
    month = today.month     
    year = today.year       
    
    
    day_words = convert(day)
    month_words = convert(month)
    year_words = convert(year)
    voice = f"Сегодня {day_words} число {month_words} месяц {year_words} года"
    return Response(voice=voice)

@manager.new("(подскажи|скажи)? (время|который час)?")
def get_time() -> Response:
    time = datetime.now()
    hour = convert(time.hour)
    minutes = convert(time.minute)
    voice = f"Сейчас {hour} час(-ов) {minutes} минут"
    return Response(voice=voice)

