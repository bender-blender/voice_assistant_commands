from stark import CommandsManager, Response
from .providers.reminders import Reminder
from .custom_types import Time,Day,Year
from stark.core.types import String


reminder_manager = CommandsManager()

reminder = Reminder()

@reminder_manager.new(r"(создай|создать|добавь|добавить) (запись|заметку|напоминание)")
def call_create_reminder():
    reminder.create_reminder()
    return Response(voice="Заметка создана")

@reminder_manager.new(r"(описание|суть|смысл) $content:String")
def call_add_summary(content:String):
    reminder.add_summary(content)
    return Response(voice="добавлено")

@reminder_manager.new(r"(дата начала|дата) $value:Day")
def call_day(value:Day):
    reminder.add_time(value)
    return Response(voice="добавлено")

@reminder_manager.new(r"(года|год|годы) $value:Year")
def call_year(value:Year):
    reminder.add_year(value)
    return Response(voice="добавлено")

@reminder_manager.new(r"время в $value:Time")
def call_hour(value:Time):
    reminder.add_time(value)
    return Response(voice="добавлено")

@reminder_manager.new(r"(место|локация) $content:String")
def call_location(content:String):
    reminder.add_location(content)
    return Response(voice="добавлено")

@reminder_manager.new(r"(сохранить|завершить)")
def call_save():
    reminder.save()
    return Response(voice="Сохранено")