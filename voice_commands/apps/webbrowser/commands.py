from .providers.provider_webbrowser import WebBrowserProvider
from stark import CommandsManager, Response
from stark.core.types import String


webbrowser_manager = CommandsManager()
browser = WebBrowserProvider()

@webbrowser_manager.new("(вопрос|запрос) $question:String")
def call_webbrowser(question: String) -> str:
    browser.open_browser(query=question)
    return Response(voice="Выполняю запрос")

# TODO: "открой сайт" command, NOTE: Google's I'm feeling lucky feature that opens the first result of a search query may be useful here
# TODO: "quick look" feature that returns text of the small summary card, check the legacy QA module for the example
# TODO: wiki / dictionary command from the legacy QA module
