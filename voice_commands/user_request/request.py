from stark import CommandsManager,Response
from pywhatkit.core.exceptions import InternetException
from stark.core.types import String
import pywhatkit
import socket

request_manager = CommandsManager()

class Request:
    """
    browser request class
    """
    def __init__(self):
        request_manager.new(r"(у меня есть|ответь на)? (вопрос|запрос) $question:String")(self.find_the_answer)
        

    @staticmethod
    def is_connect():
        try:
            socket.create_connection(("www.google.com",80),timeout=5)
            return True
        except OSError:
            return False

    def find_the_answer(self,question:String):
        if not self.is_connect():
            return Response(voice="Ответ не найден, или же отсутствует соединение")
        try:
            pywhatkit.search(question.value)
            return Response(voice="Выполняю запрос")
        except InternetException:
            return Response(voice="Ошибка сети: не удалось выполнить запрос, но работа продолжается.")
        except Exception as e:
            return Response(voice=f"Произошла ошибка: {str(e)}")