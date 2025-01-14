import anyio
from stark import run
from voice_commands import manager
from stark.interfaces.vosk import VoskSpeechRecognizer
from stark.interfaces.silero import SileroSpeechSynthesizer


recognizer = VoskSpeechRecognizer(model_url=VOSK_MODEL_URL)
synthesizer = SileroSpeechSynthesizer(model_url=SILERO_MODEL_URL)


async def main():
    await run(manager, recognizer, synthesizer)

if __name__ == "__main__":
    anyio.run(main)

    