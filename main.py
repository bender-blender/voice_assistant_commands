import anyio
from stark import run
from voice_commands import (
    manager,
    player_manager,
    #stopwatch_manager,
    #reminder_manager,
    #reminder,
    #webbrowser_manager,
    weather_manager
    )
from stark.interfaces.vosk import VoskSpeechRecognizer
from stark.interfaces.silero import SileroSpeechSynthesizer
from dotenv import load_dotenv
import os


load_dotenv("example.env")

VOSK_MODEL_URL = os.getenv("VOSK_MODEL_URL")
SILERO_MODEL_URL = os.getenv("SILERO_MODEL_URL")

recognizer = VoskSpeechRecognizer(model_url=VOSK_MODEL_URL)
synthesizer = SileroSpeechSynthesizer(model_url=SILERO_MODEL_URL)

manager.extend(player_manager)
manager.extend(weather_manager)
# reminder_manager.extend(stopwatch_manager)
# reminder_manager.extend(time_manager)
# reminder_manager.extend(webbrowser_manager)
# reminder_manager.extend(player_manager)
# reminder_manager.extend(weather_manager)

async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(run, manager, recognizer, synthesizer)
        #tg.start_soon(handle_reminders)

# async def handle_reminders():
#     async for response in reminder.reminder_loop():
#         speech = await synthesizer.synthesize(response.voice)
#         await speech.play()

if __name__ == "__main__":
    anyio.run(main)



