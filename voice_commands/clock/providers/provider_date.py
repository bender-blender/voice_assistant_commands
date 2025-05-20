from stark import Response, CommandsManager
from ..commands.command_date import DateCommands
from ..helpers.helpers import num2word


date = CommandsManager()
commands = DateCommands()

@date.new("дата")
def call_date():
    result = commands.get_date().get_formatted_date().split(" ")
    phrase = [num2word(int(i)) if i.isdigit() else i for i in result]
    return Response(voice=f"Сегодня {phrase} года")