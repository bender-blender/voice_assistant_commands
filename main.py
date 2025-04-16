import anyio
from stark import run
from voice_commands import (
    data_manager,
    Data,
    Time,
    time_manager, 
    MediaPlayer, 
    media_manager, 
    Request, 
    request_manager, 
    CityTime, 
    time_city_manager, 
    Timer, 
    timer_manager,
    State,
    Stopwatch,
    stopwatch_manager,
    Note,
    note_manager)
from stark.interfaces.vosk import VoskSpeechRecognizer
from stark.interfaces.silero import SileroSpeechSynthesizer
from stark import Response

VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
SILERO_MODEL_URL = "https://models.silero.ai/models/tts/ru/v3_1_ru.pt"

recognizer = VoskSpeechRecognizer(model_url=VOSK_MODEL_URL)
synthesizer = SileroSpeechSynthesizer(model_url=SILERO_MODEL_URL)

timer = Timer()
data_instance = Data()
city = CityTime()
time_instance = Time()
state = State()
note = Note()
stopwatch = Stopwatch()
media = MediaPlayer()
request = Request()

data_manager.extend(timer_manager)
data_manager.extend(time_city_manager)
data_manager.extend(time_manager)
data_manager.extend(note_manager)
data_manager.extend(stopwatch_manager)
data_manager.extend(media_manager)
data_manager.extend(request_manager)

async def handle_reminders():
    async for response in note.reminder_loop():
        speech = await synthesizer.synthesize(response.voice)
        await speech.play()


async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(handle_reminders)
        tg.start_soon(run, data_manager, recognizer, synthesizer)

if __name__ == "__main__":
    anyio.run(main)


