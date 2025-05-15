from stark import CommandsManager
from .notes import Note
from stark.core.types import MyYear,MyTime,MyHours,String

note_manager = CommandsManager()
note = Note()

@note_manager.new(r"(создай|создать|добавь|добавить) (запись|заметку|напоминание)")
def call_create_note():
    return note.create_a_note()

@note_manager.new(r"(описание|суть|смысл) $content:String")
def call_add_summary(content:String):
    return note.add_summary(content)

@note_manager.new(r"(дата начала|дата) $day:MyTime")
def call_day(day:MyTime):
    return note.add_time(day)

@note_manager.new(r"(года|год|годы) $year:MyYear")
def call_year(year:MyYear):
    return note.add_year(year)

@note_manager.new(r"время в $hour:MyHours")
def call_hour(hour:MyHours):
    return note.start_date(hour)

@note_manager.new(r"(место|локация) $content:String")
def call_location(content:String):
    return note.add_location(content)

@note_manager.new(r"(сохранить|завершить)")
def call_save():
    return note.save_event()