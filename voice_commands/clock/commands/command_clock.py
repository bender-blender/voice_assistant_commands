from ..models.model_time import TimeModel
from datetime import datetime

class TimeCommands:    

    def get_time(self):
        now = datetime.now()
        final_value = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute
        )
        return TimeModel(final_value)
        
