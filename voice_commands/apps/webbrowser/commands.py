from .providers.webbrowser_provider import WebBrowserProvider
from stark import CommandsManager, Response
from stark.core.types import String


webbrowser_manager = CommandsManager()
browser = WebBrowserProvider()

@webbrowser_manager.new("(вопрос|запрос) $question:String") # type: ignore
def call_webbrowser(question: String) -> str:
    browser.open_browser(query=question)
    return Response(voice="Выполняю запрос") # type: ignore