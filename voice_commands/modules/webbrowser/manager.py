from stark import CommandsManager
from .request import Request
from stark.core.types import String

request_manager = CommandsManager()
request = Request()

class Website: # custom stark type
    host: String
    domain: String
    
    # format:   <host>.<domain> или хост точка домен; ютуб точка ком

@request_manager.new(r"(у меня есть|ответь на)? (вопрос|запрос) $site:Website") # открой <сайт> в браузере
def call_find_the_answer(site:site):
    return request.open_site(question)

@request_managerr.new(r"(у меня есть|ответь на)? (вопрос|запрос) $question:String") # загугли <что-то>
def call_find_the_answer(question:String):
    return request.find_the_answer(question)

@request_manager.new(r"у меня есть|ответь на)? (вопрос|запрос)  $question:String") # быстрый гугл
def call_find_the_answer(question:String):
    return request.fast_google(question) # returns answer without browser, see the old commands from Mark
