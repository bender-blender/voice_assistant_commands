from stark import  Response
from pydbus import SessionBus
from stark.core.types import String
from word2number import w2n
from translate import Translator
import subprocess

class MediaPlayer:
    """
    Media player
    """

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
            self.player = None

    def play(self):
        if self.player:
            self.player.Play()
        else:
            return Response(voice="Медиаплеер не включен")

    def pause(self):
        if self.player:
            self.player.Pause()
        else:
            return Response(voice="Медиаплеер не включен")

    def next_track(self):
        if self.player:
            self.player.Next()
        else:
            return Response(voice="Медиаплеер не включен")

    def previous_track(self):
        if self.player:
            self.player.Previous()
            self.player.Previous()
        else:
            return Response(voice="Медиаплеер не включен")

    def set_volume(self, vol: String):
        try:
            print("Выполняю")
            num = Translator(to_lang="en", from_lang="ru").translate(vol.value)
            num = w2n.word_to_num(num)
        # Преобразование входного параметра в строку
            volume = max(0, min(num, 100))  # Ограничение в пределах 0-100
            subprocess.run(["amixer", "sset", "Master", f"{volume}%"])
            print(f"Системная громкость установлена на {volume}%.")

        except ValueError as e:
            print(f"Ошибка преобразования текста в число: {e}")
            return Response(voice="Не удалось распознать указанную громкость. Попробуйте снова.")

        except AttributeError as e:
            print(f"Ошибка доступа к плееру: {e}")
            return Response(voice="Плеер не найден или не поддерживает управление громкостью.")

        except Exception as e:
            print(f"Неожиданная ошибка ({type(e)}): {e}")
            return Response(voice="Произошла ошибка при установке громкости.")

    def maximum(self):
        volume = 100
        subprocess.run(["amixer", "sset", "Master", f"{volume}%"])
        print(f"Системная громкость установлена на {volume}%.")

    def minimum(self):
        volume = 20  
        subprocess.run(["amixer", "sset", "Master", f"{volume}%"])
        print(f"Системная громкость установлена на {volume}%.")

    def turn_off_the_sound(self):
        volume = 0 
        subprocess.run(["amixer", "sset", "Master", f"{volume}%"])
        print(f"Системная громкость установлена на {volume}%.")

    def get_info(self):
        if not self.player:
            return Response(voice="Медиаплеер не найден.")
        metadata = self.player.Metadata
        track_name = metadata.get("xesam:title", "Неизвестно")
        # Проверяем наличие артиста и возвращаем первое имя, если оно есть, или дефолтное значение
        artist_name = metadata.get("xesam:artist", ["Неизвестен"])[
            0] if metadata.get("xesam:artist") else "Неизвестен"
        album_name = metadata.get("xesam:album", "Неизвестен")

        print(
            f"Сейчас играет: {track_name} — {artist_name} (Альбом: {album_name})")
