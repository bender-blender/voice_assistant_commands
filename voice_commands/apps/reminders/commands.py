from stark import CommandsManager, Response
from .providers.reminders import Reminder
from .custom_types import Day, Time, Year
from stark.core.types import String


reminder_manager = CommandsManager()

reminder = Reminder()

# TODO: refactor to use command context

@reminder_manager.new(r"(создай|создать|добавь|добавить) (запись|заметку|напоминание)")
def call_create_reminder():
    reminder.create_reminder()
    return Response(voice="Заметка создана")

@reminder_manager.new(r"(описание|суть|смысл) $content:String")
def call_add_summary(content:String):
    reminder.add_summary(content)
    return Response(voice="добавлено")

@reminder_manager.new(r"(дата начала|дата) $value:Day")
def call_day(value: Day):
    reminder.add_date(value)
    return Response(voice=f"Дата добавлена")

@reminder_manager.new(r"(время|время начала) $value:Time")
def call_time(value: Time):
    reminder.add_time(value)
    return Response(voice=f"Время добавлено")

@reminder_manager.new(r"год $value:Year")
def call_year(value: Year):
    reminder.add_year(value)
    return Response(voice=f"Год добавлен")

@reminder_manager.new(r"(место|локация|адрес) $content:String")
def call_location(content: String):
    reminder.add_location(content)
    return Response(voice="Место добавлено")

@reminder_manager.new(r"(сохранить|завершить|готово)")
def call_save_reminder():
    print("Сохраняем заметку — возвращаем ответ")
    reminder.save()
    return Response(voice="Заметка сохранена")
