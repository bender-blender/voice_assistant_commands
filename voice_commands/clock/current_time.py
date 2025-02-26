from datetime import datetime
from stark import CommandsManager, Response
from dependencies.auxiliary_functions import convert

time_manager = CommandsManager()


class Time:
    """time class."""
    
    def __init__(self):
        patterns = [
            r"(подскажи|скажи|сколько) времени?",  
            r"(какое|текущее) время",  
            r"сколько сейчас (времени|часов)",  
            r"который час",  
            r"сколько времени на часах",  
            r"назови текущее время",  
            r"мне нужно узнать время",  
            r"какое сейчас время суток",  
            r"уточни время"  
        ]
        
        for pattern in patterns:
            time_manager.new(pattern)(self.show_time)
    
    def show_time(self):
        current_time = datetime.now()
        hours = current_time.hour
        minutes = current_time.minute
        
        response_text = f"Сейчас {convert(hours)} часов {convert(minutes)} минут"
        return Response(voice=response_text)