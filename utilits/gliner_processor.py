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
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1" # TODO: document
logging.set_verbosity_error() # __main__.py or CLI parameter
warnings.filterwarnings("ignore") # same as logs


class GliNERProcessor(CommandsContextProcessor):

    def __init__(self):
        self.labels = [
            "location",
            "organization",
        ]
        self.model = GLiNER.from_pretrained("urchade/gliner_multi") # TODO: document

    async def process_string(self, string: str, context: CommandsContext, recognized_entities: list[RecognizedEntity]):
        normal_form = [word for word in string.split()]
        entities = self.model.predict_entities(text=" ".join(
            normal_form), labels=self.labels)
        await anyio.sleep(0.1)
         

        for entitie in entities:
            if not entitie:
                continue
            entity = RecognizedEntity(
                entitie["text"], # cut substr
                type=NLLocation, # the custom class to call parsing and the did_parse
                # key=entitie["score"]
            )
            print(entity) # TODO: use logs or remove
            if entitie["score"] >= 0.75:
                recognized_entities.append(entity)
            
    def clear_recognized_entities(self, recognized_entities: list[RecognizedEntity]):
        recognized_entities.clear()
    
   

