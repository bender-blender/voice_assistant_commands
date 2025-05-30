from ..custom_types.custom_sound import Sound
from pydbus import SessionBus
from stark import  Response
import subprocess


class MediaPlayerProvider:

    def __init__(self):
        session_bus = SessionBus()
        dbus_service = session_bus.get(
            "org.freedesktop.DBus", "/org/freedesktop/DBus")
        services = dbus_service.ListNames()
        mpris_services = [service for service in services if service.startswith(
            "org.mpris.MediaPlayer2.")]
        if mpris_services:
            self.player = session_bus.get(
                mpris_services[0], "/org/mpris/MediaPlayer2")
        else:
            raise Exception("Отсутствует доступный медиаплеер")

    def play(self):        
        self.player.Play()

    def pause(self):
        self.player.Pause()
        
    def next_track(self):        
        self.player.Next()

    def previous_track(self):        
        self.player.Previous()
        self.player.Previous()
    
    def set_volume(self, volume: Sound):
        try:
            volume = max(0, min(volume.volume, 100))  
            subprocess.run(["amixer", "sset", "Master", f"{volume}%"])
            return volume

        except ValueError as e:
            return Response(voice="Не удалось распознать указанную громкость. Попробуйте снова.")
    
    def get_info(self):
        
        metadata = self.player.Metadata
        track_name = metadata.get("xesam:title", None)
        artist_name = metadata.get("xesam:artist", [None])[
            0] if metadata.get("xesam:artist") else None

        print(
            f"Сейчас играет: {track_name} — {artist_name}")
