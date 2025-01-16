import pywhatkit as kit
from stark.core.types import String
from stark import CommandsManager, Response

request_manager = CommandsManager()
@request_manager.new(r'(ответить|ответь|у меня есть) (на запрос|на вопрос|запрос|вопрос) $query:String')
def answer(query: String) -> Response:
    try:
        kit.search(query)
        return Response(voice="Отрабатываю запрос")
    except:
        return Response(voice="Ошибка, попробуйте еще раз")
