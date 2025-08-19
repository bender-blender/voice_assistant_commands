from stark import CommandsManager, Response
from stark.core import ResponseHandler
from stark.core.types import String
from .provider.alarm_provider import ProviderAlarm
from voice_commands.parameters import Time


alarm_manager = CommandsManager()
alarm = ProviderAlarm()


@alarm_manager.new("(поставь|заведи) будильник")
def call_create_alarm():
    return Response(voice="Название?", commands=[call_add_name])


@alarm_manager.new("$name:String", hidden=True)
def call_add_name(name: String, **params) -> Response:
    alarm.add_name(name)
    return Response(
        voice="Добавим время",
        parameters={**params, "name": name.value},
        commands=[call_add_time]
    )


@alarm_manager.new("$time:Time", hidden=True)
def call_add_time(time: Time, **params) -> Response:
    alarm.add_target_time(time)
    return Response(
        voice="Добавим день",
        parameters={**params, "time": time.value},
        commands=[call_add_day]
    )


@alarm_manager.new("$day:String", hidden=True)
def call_add_day(day: String, **params) -> Response:
    alarm.add_day(day)
    return Response(
        voice="Сохранить?",
        parameters={**params, "day": day.value},
        commands=[call_save_alarm]
        )


@alarm_manager.new("(да|сохрани|сохранить)", hidden=True)
def call_save_alarm(handler: ResponseHandler, **params):
    alarm.start_alarm()
    while True:
        try:
            handler.pop_context()
        except Exception:
            break
    return Response(voice="Будильник сохранен.")



@alarm_manager.new("(удалить|удали) (будильник)? $name:String")
def call_del_alarm(name:String):
    alarm.cancel_alarm(name)
    return Response(voice="Будильник удален")

@alarm_manager.new("посмотри будильники")
def call_get_alarm():
    alarms = alarm.get_alarm()
    if not alarms:
        return Response(voice="Будильников нет")

    for k,v in alarms.items():
        print(f"Будильник: {k}, Время: {v[0]}, День: {v[1]}")
    return Response(voice="Все будильники")
