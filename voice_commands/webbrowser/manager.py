from .providers.provider_webbrowser import WebBrowserProvider
from stark import CommandsManager, Response
from stark.core.types import String
import webbrowser

webbrowser_manager = CommandsManager()

request = WebBrowserProvider()

@webbrowser_manager.new("(вопрос|запрос) $question:String")
def call_webbrowser(question: String) -> str:
    webbrowser.open(request.search(question))
    return Response(voice="Выполняю запрос")