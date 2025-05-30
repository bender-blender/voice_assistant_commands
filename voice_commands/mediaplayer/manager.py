from .providers.provider_player import MediaPlayerProvider
from .custom_types.custom_sound import Sound
from stark import Response, CommandsManager


player_manager = CommandsManager()
media = MediaPlayerProvider()

@player_manager.new("(медиа|медиаплеер|плеер|музыка|)")
def call_play_media():
    media.play()
    

@player_manager.new("(пауза|пауза медиа|пауза плеер|пауза музыка|)")
def call_pause_media():
    media.pause()
    

@player_manager.new("(следующий трек|следующий трек медиа|следующий трек плеер|следующий трек музыка|)")
def call_next_track():
    media.next_track()
    

@player_manager.new("(предыдущий трек|предыдущий трек медиа|предыдущий трек плеер|предыдущий трек музыка|)")
def call_previous_track():
    media.previous_track()
    

@player_manager.new("громкость $volume_percentages:Sound")
def call_set_volume(volume_percentages: Sound):
    media.set_volume(volume_percentages)
    

@player_manager.new("информация")
def call_get_info():
    media.get_info()
    