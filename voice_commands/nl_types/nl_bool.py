from stark.core.patterns import Pattern, ParseError
from stark.core.types import Object
from stark.general.classproperty import classproperty
from voice_commands.helpers.confirmation_phrases import confirmations,rejections
from voice_commands.helpers.detect_lang import identify_the_language
from translate import Translator


class NLBool(Object):
    value: bool
    
    @classproperty
    def pattern(cls) -> Pattern:
        return Pattern("**")
    

    async def did_parse(self, from_string: str) -> str:
        from_string = from_string.lower()
        
        lang_code = identify_the_language(from_string)
        translator = Translator(
            from_lang=lang_code,
            to_lang="ru").translate(from_string).lower().replace(".","")
        
        if translator in confirmations:
            self.value = True
            return from_string
        
        if translator in rejections:
            self.value = False
            return from_string
        

        raise ParseError("Failed to determine phrase")