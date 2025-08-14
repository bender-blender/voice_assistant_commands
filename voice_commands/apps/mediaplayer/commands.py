from stark import CommandsManager

from .parameters.volume import Volume
from .providers.provider_player import MediaPlayerProvider

player_manager = CommandsManager()
media = MediaPlayerProvider()


@player_manager.new("(медиа|медиаплеер|плеер|музыка)")
def call_play_media():
    print("Воспроизведение медиа")
    media.play()


@player_manager.new("(пауза|пауза медиа|пауза плеер|пауза музыка|стоп)")
def call_pause_media():
    media.pause()


@player_manager.new("(следующий трек|следующий трек медиа|следующий трек плеер|следующий трек музыка)")
def call_next_track():
    media.next_track()


@player_manager.new("(предыдущий трек|предыдущий трек медиа|предыдущий трек плеер|предыдущий трек музыка)")
def call_previous_track():
    media.previous_track()


@player_manager.new("громкость $volume_percentages:Volume")
def call_set_volume(volume_percentages: Volume):
    media.set_volume(volume_percentages)


@player_manager.new("информация")
def call_get_info():
    media.get_info()
