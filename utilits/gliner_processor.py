from stark.core.processors.spacy_ner_processor import CommandsContextProcessor
from stark.core.parsing import RecognizedEntity
from stark import CommandsContext
from gliner import GLiNER
import anyio

from voice_commands.nl_types.nl_location.nl_location import NLLocation
from transformers import logging


class GliNERProcessor(CommandsContextProcessor):
    _model = None

    def __init__(self):
        self.labels = [
            "location",
            "organization",
        ]
        
        if GliNERProcessor._model is None:
            GliNERProcessor._model = GLiNER.from_pretrained("urchade/gliner_multi")


    async def process_string(self, string: str, context: CommandsContext, recognized_entities: list[RecognizedEntity]):
        normal_form = [word for word in string.split()]
        entities = self._model.predict_entities(text=" ".join(
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
            if entitie["score"] >= 0.75:
                recognized_entities.append(entity)
            
    def clear_recognized_entities(self, recognized_entities: list[RecognizedEntity]):
        recognized_entities.clear()
    
   

