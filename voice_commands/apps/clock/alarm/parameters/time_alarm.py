from stark.core.patterns import Pattern
from stark.core.types import Object, ParseError
from stark.general.classproperty import classproperty
from typing import Tuple, List
import schedule



class WeekDay(Object):

    value: List[Tuple[str, schedule.Job]]

    @classproperty
    def pattern(cls):
        return Pattern("**")
    

    async def did_parse(self, from_string: str) -> str:
        list_of_days = []
        if from_string == "каждый день":
            create_task = schedule.every().day
            list_of_days.append((from_string,create_task))

        for days in from_string.split(" "):
            day = days.lower()
            if "понедельник" in day:
                create_task = schedule.every().monday
            elif "вторник" in day:
                create_task = schedule.every().tuesday
            elif "сред" in day:
                create_task = schedule.every().wednesday
            elif "четверг" in day:
                create_task = schedule.every().thursday
            elif "пятниц" in day:
                create_task = schedule.every().friday
            elif "суббот" in day:
                create_task = schedule.every().saturday
            elif "воскресенье" in day:
                create_task = schedule.every().sunday
            list_of_days.append((day,create_task))
        
        self.value = list_of_days
        if self.value is None:
            raise ParseError(f"Failed to create task for day: {from_string}")
        
        return from_string

Pattern.add_parameter_type(WeekDay)