from stark import CommandsManager
from .request import Request
from stark.core.types import String

request_manager = CommandsManager()
request = Request()

@request_manager.new(r"(у меня есть|ответь на)? (вопрос|запрос) $question:String")
def call_find_the_answer(question:String):
    return request.find_the_answer(question)
