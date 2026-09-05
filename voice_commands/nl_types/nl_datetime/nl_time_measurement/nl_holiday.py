from stark.core.parsing import Pattern, ParseError, ObjectParser, PatternParser
from stark.general.classproperty import classproperty
from stark.general.localisation import LocaleString
from stark.core.types import Object
from icalendar import Calendar

from voice_commands.nl_types.parsing_context import pattern_parser
from datetime import datetime


class Link:

    def __init__(self,links:list[str] = []) -> None:
        self.storage_link = links


    def add(self,value):
        if not isinstance(value,str):
            return 
          
        self.storage_link.append(value)


    def read(self):
        return self.storage_link

    def remove(self,value):
        if value not in self.storage_link:
            return

        self.storage_link.remove(value)



        
class Event:

    def __init__(self, link: Link) -> None:
        index = 1

        for i in link.storage_link:
            with open(i, "rb") as file:
                calendar = Calendar.from_ical(file.read())

            for event in calendar.walk("VEVENT"):
                name = str(event.get("summary")).lower()
                start = str(event.get("dtstart").dt)
                end = str(event.get("dtend").dt)
                self.__dict__[str(index)] = (name,datetime.fromisoformat(start),datetime.fromisoformat(end))
                index += 1
    



class NLHoliday(Object):
    value: int
    event: Event | None = None

    @classproperty
    def pattern(cls) -> Pattern:
        if cls.event is None:
            raise ValueError("Event is not set")
        
        values = list(cls.event.__dict__.values())
        if not values:
            raise ValueError("Event has no attributes")

        pattern_list = [i[0] for i in values]
        pattern = "(" + "|".join(pattern_list) + ")"
        return Pattern(pattern)

    def resolve(self):
        return self.event.__dict__[str(self.value)][1:3]



class NLHolidayParser(ObjectParser):

    def __init__(self,pattern:PatternParser,event:Event) -> None:
        self.pattern = pattern
        self.link = Link()
        self.event = event

    async def did_parse(self, obj: NLHoliday, from_string: LocaleString) -> str:
        for key,value in self.event.__dict__.items():
            if value[0] in from_string:
                obj.value = int(key)
                return from_string 
            
        raise ParseError("event not found!")

link_list = Link([
    "/home/bender/voice_assistant_commands/voice_commands/math.ics",
    "/home/bender/voice_assistant_commands/voice_commands/morning_routine.ics",
    "/home/bender/voice_assistant_commands/voice_commands/weekly_reset.ics"
])
    
events = Event(link_list)



NLHoliday.event = events

pattern_parser.register_parameter_type(
    NLHoliday,
    NLHolidayParser(
        pattern_parser,
        events
    )
)
