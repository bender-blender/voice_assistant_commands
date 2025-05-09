from stark import CommandsManager
from .media import MediaPlayer
from stark.core.types import String


media_manager = CommandsManager()
media = MediaPlayer()

@media_manager.new(r"(включи песню|включи музыку|включи трек|включи песню|включи песни|включи)")
def call_media():
    return media.play()


@media_manager.new(r"(выключи|выключи музыку|выключи трек|выключи песню|стоп)")
def call_stop():
    return media.pause()


@media_manager.new(r"(следующий трек|дальше|вперёд|)")
def call_next():
    return media.next_track()

@media_manager.new(r"(предыдущий трек|назад)")
def call_previous():
    return media.previous_track()

@media_manager.new(r"сделай громкость на $vol:String")
def call_set_volume(vol:String):
    return media.set_volume(vol)


@media_manager.new(r"(установи громкость на сто|поставь звук на полную мощность|громкость на полную|максимальный уровень звука|поставь звук на максимум|сделай громкость на полную|включи звук на максимум|звук на пределе|выставь максимальную громкость)")
def call_maxim():
    return media.maximum()

@media_manager.new(r"(уменьши громкость до минимума|поставь звук на минимум|выставь минимальный уровень громкости|поставь звук на самый низкий уровень)")
def call_minimum():
    return media.minimum()

@media_manager.new(r"(звук на нуле|убавь громкость до конца|отключи звук|уменьши громкость до нуля)")
def call_turn_off_the_sound():
    return media.turn_off_the_sound()

@media_manager.new(r"(про песню|про трек|что сейчас играет|информация)")
def call_info():
    return media.get_info()