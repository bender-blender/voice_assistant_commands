from voice_commands.nl_types.nl_bool.nl_bool_interface import NLBoolParseLanguage


class NLBoolParseRu(NLBoolParseLanguage):
    def __init__(self):
        super().__init__(
            confirmations=[
                "да", "конечно", "ага", "угу", "хорошо", "ладно", "окей",
                "верно", "точно", "правильно", "подтверждаю", "так и есть",
                "сделай", "можно", "пусть будет"
            ],
            rejections=[
                "нет", "не надо", "не сейчас", "отмена", "стоп", "не нужно",
                "откажись", "лучше не стоит", "потом", "не соглашусь", "не хочу",
                "ни за что", "не совсем", "не особо"
            ],
        )

    
class NLBoolParseEn(NLBoolParseLanguage):
    def __init__(self):
        super().__init__(
            confirmations=[
                "yes", "yeah", "yep", "sure", "of course", "ok",
                "okay", "alright", "right", "correct", "confirmed",
                "that's true", "do it", "go ahead", "you can",
                "sounds good", "fine"
            ],
            rejections=[
                "no", "nope", "not now", "cancel", "stop", "don't",
                "don't do it", "better not", "later", "i disagree",
                "i don't want to", "no way", "not really",
                "not quite", "not necessary"
            ],
        )
