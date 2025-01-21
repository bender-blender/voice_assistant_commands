import pywhatkit as kit
from stark.core.types import String
from stark import CommandsManager, Response
import socket
request_manager = CommandsManager()
# Функция для проверки наличия интернета
def is_connected():
    try:
        # Пытаемся подключиться к Google (или любому другому известному серверу)
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

@request_manager.new(r'(ответить|ответь|у меня есть) (на запрос|на вопрос|запрос|вопрос) $query:String')
def answer(query: String) -> Response:
    if not is_connected():
        return Response(voice="Нет подключения к интернету. Пожалуйста, проверьте соединение.")
    else:
        try:
            kit.search(query)
            return Response(voice="Отрабатываю запрос")
        except:
            return Response(voice="Ошибка, попробуйте еще раз")
