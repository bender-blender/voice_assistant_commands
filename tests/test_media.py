import pytest
from unittest.mock import patch, MagicMock
from voice_commands import MediaPlayer  # Предполагаем, что класс сохранён в media_player.py
from stark.core.types import String


def test_play():
    player = MediaPlayer()
    player.player = MagicMock()
    player.play()
    player.player.Play.assert_called_once()

def test_pause():
    player = MediaPlayer()
    player.player = MagicMock()
    player.pause()
    player.player.Pause.assert_called_once()

def test_next_track():
    player = MediaPlayer()
    player.player = MagicMock()
    player.next_track()
    player.player.Next.assert_called_once()

def test_previous_track():
    player = MediaPlayer()
    player.player = MagicMock()
    player.previous_track()
    assert player.player.Previous.call_count == 2

@patch("subprocess.run")
def test_set_volume(mock_subprocess):
    player = MediaPlayer()
    with patch("voice_commands.user_media.media.Translator.translate", return_value="50"), \
         patch("voice_commands.user_media.media.w2n.word_to_num", return_value=50):
        response = player.set_volume(String("пятьдесят"))
    
    mock_subprocess.assert_called_with(["amixer", "sset", "Master", "50%"])
    assert response is None  # Метод не должен возвращать ошибку

@patch("subprocess.run")
def test_maximum(mock_subprocess):
    player = MediaPlayer()
    player.maximum()
    mock_subprocess.assert_called_with(["amixer", "sset", "Master", "100%"])

@patch("subprocess.run")
def test_minimum(mock_subprocess):
    player = MediaPlayer()
    player.minimum()
    mock_subprocess.assert_called_with(["amixer", "sset", "Master", "20%"])

@patch("subprocess.run")
def test_turn_off_the_sound(mock_subprocess):
    player = MediaPlayer()
    player.turn_off_the_sound()
    mock_subprocess.assert_called_with(["amixer", "sset", "Master", "0%"])

def test_get_info():
    player = MediaPlayer()
    player.player = MagicMock()
    player.player.Metadata = {
        "xesam:title": "Test Song",
        "xesam:artist": ["Test Artist"],
        "xesam:album": "Test Album"
    }

    with patch("builtins.print") as mock_print:
        player.get_info()
        mock_print.assert_called_with("Сейчас играет: Test Song — Test Artist (Альбом: Test Album)")
