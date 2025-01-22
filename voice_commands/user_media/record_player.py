from pydbus import SessionBus
import anyio
from stark import Response, CommandsManager
from stark.core.types import String
from word2number import w2n
from translate import Translator
import subprocess
# Подключаемся к шине SessionBus (пользовательская сессия)

media = CommandsManager()


bus = SessionBus()
dbus_service = bus.get("org.freedesktop.DBus", "/org/freedesktop/DBus")
services = dbus_service.ListNames()
mpris_services = [service for service in services if service.startswith("org.mpris.MediaPlayer2.")]
print("Доступные MPRIS плееры:", mpris_services)

player = None
if mpris_services:
    # Выбираем первый найденный плеер
    player = bus.get(mpris_services[0], "/org/mpris/MediaPlayer2")
else:
    print("Не найдено активных MPRIS плееров.")
    
@media.new("(включи песню|включи музыку|включи трек|включи песню|включи песни|включи)")
async def play():
    player.Play()
    await anyio.sleep(1)
    

@media.new("(выключи|выключи музыку|выключи трек|выключи песню|стоп)")
async def pause():
    player.Pause()
    await anyio.sleep(1)
    

@media.new("(следующий трек|дальше|вперед|)")
async def next_track():
    player.Next()
    await anyio.sleep(1)
    

@media.new("(предыдущий трек|назад)")
async def next_track():
    player.Previous()
    player.Previous()
    await anyio.sleep(1)
    


@media.new("сделай громкость на $vol1:String")
async def set_volume(vol1: String):
    
    try:
        num = Translator(to_lang="en", from_lang="ru").translate(vol1.value)
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

@media.new(r"(установи громкость на сто|поставь звук на полную мощность|громкость на полную|максимальный уровень звука|поставь звук на максимум|сделай громкость на полную|включи звук на максимум|звук на пределе|выставь максимальную громкость)")
async def maximum():
    volume = 100  # Ограничение в пределах 0-100
    await anyio.sleep(1)
    subprocess.run(["amixer", "sset", "Master", f"{volume}%"])
    print(f"Системная громкость установлена на {volume}%.")

@media.new(r"(уменьши громкость до минимума|поставь звук на минимум|звук на нуле|убавь громкость до конца|отключи звук|выставь минимальный уровень громкости|уменьши громкость до нуля|поставь звук на самый низкий уровень)")
async def minimum() :
    volume = 0  # Ограничение в пределах 0-100
    await anyio.sleep(1)
    subprocess.run(["amixer", "sset", "Master", f"{volume}%"])
    print(f"Системная громкость установлена на {volume}%.")

@media.new("(про песню|про трек|что сейчас играет|информация)")
async def get_info():
    metadata = player.Metadata
    track_name = metadata.get("xesam:title", "Неизвестно")
    await anyio.sleep(1)    
        # Проверяем наличие артиста и возвращаем первое имя, если оно есть, или дефолтное значение
    artist_name = metadata.get("xesam:artist", ["Неизвестен"])[0] if metadata.get("xesam:artist") else "Неизвестен"
    album_name = metadata.get("xesam:album", "Неизвестен")
        
    print(f"Сейчас играет: {track_name} — {artist_name} (Альбом: {album_name})")

