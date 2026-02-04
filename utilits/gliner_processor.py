from stark.core.processors.spacy_ner_processor import CommandsContextProcessor
from stark.core.parsing import RecognizedEntity
from pymorphy3 import MorphAnalyzer
from stark import CommandsContext
from gliner import GLiNER
import anyio


import os
import warnings
from transformers import logging

from huggingface_hub.utils.tqdm import disable_progress_bars
disable_progress_bars()
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
logging.set_verbosity_error()
warnings.filterwarnings("ignore")


class GliNERProcessor(CommandsContextProcessor):

    def __init__(self):
        self.labels = [
            "location",
            "organization",
        ]
        self.model = GLiNER.from_pretrained("urchade/gliner_multi")

    async def process_string(self, string: str, context: CommandsContext, recognized_entities: list[RecognizedEntity]):
        normal_form = [word for word in string.split()]
        entities = self.model.predict_entities(text=" ".join(
            normal_form), labels=self.labels)
        await anyio.sleep(0.1)
         

        for entitie in entities:
            if not entitie:
                continue
            print(RecognizedEntity(entitie["text"], type=entitie["label"], key=entitie["score"]))
            if entitie["score"] >= 0.75:
                recognized_entities.append(RecognizedEntity(
                    entitie["text"], type=entitie["label"]))
                    
            
    def clear_recognized_entities(self, recognized_entities: list[RecognizedEntity]):
        recognized_entities.clear()
    
   

