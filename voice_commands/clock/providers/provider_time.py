from stark import Response, CommandsManager
from ..commands.command_clock import TimeCommands
from ..helpers.helpers import num2word


time = CommandsManager()
commands = TimeCommands()

@time.new("время")
def call_time():
    result = commands.get_time().get_formatted_time().split(":")
    hour = num2word(int(result[0]))
    minute = num2word(int(result[1]))
    sentence = f"{hour} {minute} "
    #print(sentence)
    return Response(voice=sentence)
