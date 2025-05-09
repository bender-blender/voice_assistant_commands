from datetime import datetime
from stark import CommandsManager, Response
from dependencies.auxiliary_functions import convert

time_manager = CommandsManager()


class Time:
    """time class."""
    
    
    def show_time(self):
        current_time = datetime.now()
        hours = current_time.hour
        minutes = current_time.minute
        
        response_text = f"Сейчас {convert(hours)} часов {convert(minutes)} минут"
        return Response(voice=response_text)