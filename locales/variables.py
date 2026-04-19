from .translator import Translator
from dotenv import load_dotenv
import os

translator = Translator()
translator.scan_script()
load_dotenv("lang.env")
translator.change_language(os.getenv("lang"))
translator.create_translation("en", "en_US.UTF-8")
translator.create_translation("ru", "ru_RU.UTF-8")
