import anyio
from stark import run 
from voice_commands import manager,request_manager,timer,time_city,media
from stark.interfaces.vosk import VoskSpeechRecognizer
from stark.interfaces.silero import SileroSpeechSynthesizer
SILERO_MODEL_URL = "https://models.silero.ai/models/tts/ru/v3_1_ru.pt"
VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
recognizer = VoskSpeechRecognizer(model_url=VOSK_MODEL_URL)
synthesizer = SileroSpeechSynthesizer(model_url=SILERO_MODEL_URL)

manager.extend(request_manager)
manager.extend(timer)
manager.extend(time_city)
manager.extend(media)
async def main():
   await run(manager, recognizer, synthesizer)



if __name__ == "__main__":
    anyio.run(main)

