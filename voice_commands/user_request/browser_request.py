from stark import Response
from voice_commands import manager
import pywhatkit as kit
@manager.new(r"(найди|поискать|искать)\s+(.+)")
def get_an_answer() -> Response:
    query = match.group(2)
    print(query)
    return Response(voice=f"{query}")
    