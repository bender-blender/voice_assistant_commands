import anyio
from stark import run
from voice_commands import (
    time_manager,
    timer_manager,
    media_manager,
    request_manager,
    note_manager,
    note,
    weather_manager)
from stark.interfaces.vosk import VoskSpeechRecognizer
from stark.interfaces.silero import SileroSpeechSynthesizer


VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
SILERO_MODEL_URL = "https://models.silero.ai/models/tts/ru/v3_1_ru.pt"

recognizer = VoskSpeechRecognizer(model_url=VOSK_MODEL_URL)
synthesizer = SileroSpeechSynthesizer(model_url=SILERO_MODEL_URL)

time_manager.extend(timer_manager)
time_manager.extend(media_manager)
time_manager.extend(request_manager)
time_manager.extend(weather_manager)
time_manager.extend(note_manager)

async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(run, time_manager, recognizer, synthesizer)
        tg.start_soon(handle_reminders)

async def handle_reminders():
    async for response in note.reminder_loop():
        speech = await synthesizer.synthesize(response.voice)
        await speech.play()

if __name__ == "__main__":
    anyio.run(main)



