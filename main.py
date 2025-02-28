import anyio
from stark import run
from voice_commands import data_manager, Data, Time, time_manager, MediaPlayer, media_manager, Request, request_manager
from stark.interfaces.vosk import VoskSpeechRecognizer
from stark.interfaces.silero import SileroSpeechSynthesizer


VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
SILERO_MODEL_URL = "https://models.silero.ai/models/tts/ru/v3_1_ru.pt"

recognizer = VoskSpeechRecognizer(model_url=VOSK_MODEL_URL)
synthesizer = SileroSpeechSynthesizer(model_url=SILERO_MODEL_URL)

data_instance = Data()
time_instance = Time()
media = MediaPlayer()
request = Request()


data_manager.extend(time_manager)
data_manager.extend(media_manager)
data_manager.extend(request_manager)
async def main():
    await run(data_manager, recognizer, synthesizer)

if __name__ == "__main__":
    anyio.run(main)
