from stark import CommandsManager, Response
from stark.core import ResponseHandler
from stark.core.types import String

from voice_commands.parameters import Day,Time
from .providers.reminders_provider import RemindersProvider

reminders_manager = CommandsManager()
reminder = RemindersProvider()


@reminders_manager.new("(создай|создать|сделай) (заметку|напоминание)")
def call_create_reminder():
    reminder.create_reminder()
    return Response(voice="Добавим описание?", commands=[call_add_summary])


@reminders_manager.new("$summary:String", hidden=True)
def call_add_summary(summary: String, **params):
    reminder.add_summary(summary)
    return Response(
        voice="Добавим дату?",
        parameters={**params, "summary": summary.value},
        commands=[call_add_day],
    )


@reminders_manager.new("$date:Day", hidden=True)
def call_add_day(date: Day, **params):
    reminder.add_date(date)
    return Response(
        voice="Укажи время.",
        parameters={**params, "date": date.value},
        commands=[call_add_time],
    )


@reminders_manager.new("$time:Time", hidden=True)
def call_add_time(time: Time, **params):
    reminder.add_time(time)
    return Response(
        voice="Где это будет",
        parameters={**params, "time": time.value},
        commands=[call_add_location],
    )


@reminders_manager.new("$location:String", hidden=True)
def call_add_location(location: String, **params):
    reminder.add_location(location)
    return Response(
        voice="Сохраняю?",
        parameters={**params, "location": location.value},
        commands=[call_save_reminder],
    )


@reminders_manager.new("(да|сохрани|сохранить)", hidden=True)
def call_save_reminder(handler: ResponseHandler, **params):
    
    reminder.save()
    while True:
        try:
            handler.pop_context()
        except Exception:
            break
    return Response(voice="Заметка сохранена.")
