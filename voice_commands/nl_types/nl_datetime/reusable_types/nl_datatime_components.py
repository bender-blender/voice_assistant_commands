from stark.core.parsing import Pattern,ParseError
from stark.core.types import NLObject
from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString

from .nl_clock import NLClockTime
from .nl_calendar_date import NLCalendarDate

from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_relative_day import (
    NLRelativeDay,
    NLToday,
)
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_day_part import (
    NLDayPartUnion,
    NLDayPart_Morning,
)
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_week_day import (
    NLWeekDay,
)
from voice_commands.nl_types.nl_datetime.nl_time_measurement.nl_holiday import (
    NLHoliday,
)
from voice_commands.nl_types.parsing_context import pattern_parser



from datetime import datetime
from typing import Literal

import logging
import inspect

class NLDateComponents(NLObject):
    value: str

    calendar_date: NLCalendarDate | None = None

    day: NLRelativeDay | None = None
    clock: NLClockTime | None = None
    part: NLDayPartUnion | NLDayPart_Morning = None

    event: NLHoliday | None = None
    weekday: NLWeekDay | None = None

    now = datetime.now()


    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern(
            "(( )?$calendar_date:NLCalendarDate)?"
            "(( )?$day:NLRelativeDay)?"
            "(( )?$event:NLHoliday)?"
            "(( )?$weekday:NLWeekDay)?"
            "(( )?$clock:NLClockTime)?"
            "(( )?$part:NLDayPartUnion)?"
        )
    
    
    async def did_parse(self, from_string: LocaleString) -> str:
                
        if self.clock is None:
            self.clock = NLClockTime("09:00")
                    
        components = [
            self.calendar_date,
            self.day,
            self.event,
            self.weekday,
            self.clock,
            self.part,
            ]
        
        if not any(component is not None for component in components):
            raise ParseError("No datetime components found")
        
        
        logging.debug("calendar_date:", self.calendar_date)
        logging.debug("day:", self.day)
        logging.debug("event:", self.event)
        logging.debug("weekday:", self.weekday)
        logging.debug("clock:", self.clock)
        logging.debug("part:", self.part)

        self.value = " ".join(
            str(component.value)
            for component in components
            if component is not None
        )

        return from_string


    def resolve(self,mode: Literal["Last", "This", "Next"] = "This"):

        necessary_components = [
            self.calendar_date,
            self.day,
            self.event,
            self.weekday,
            self.clock,
            self.part]

        full_date = []
        for component in necessary_components:
            if component == None:
                continue

            signature_resolve = inspect.signature(component.resolve).parameters
            if "resolve" in component.__dir__() and "mode" in signature_resolve:
                
                return component.resolve(mode)
        
        return None



        

    
pattern_parser.register_parameter_type(
    NLDateComponents
)