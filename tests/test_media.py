import pytest
from unittest.mock import patch
from voice_commands import MediaPlayer, media_manager  # Предполагаем, что класс сохранён в media_player.py
from stark.core.types import String
from time import sleep

@pytest.fixture(scope="class")
def general_player():
    player = MediaPlayer()
    return player

@pytest.mark.usefixtures("general_player")
class TestMediaPlayer:

    def test_play(self, general_player):
        player = general_player
        player.play()
        sleep(3)
    
    def test_pause(self, general_player):
        player = general_player
        player.pause()
        sleep(1)

    def test_next_track(self, general_player):
        player = general_player
        player.next_track()
        sleep(1)
    
    def test_previous_track(self, general_player):
        player = general_player
        player.previous_track()
        sleep(1)
    


    @patch("subprocess.run")
    def test_set_volume(self, mock_run, general_player):  # Добавили mock_run как второй аргумент
        player = general_player
        with patch("voice_commands.user_media.media.Translator.translate", return_value="50"), \
            patch("voice_commands.user_media.media.w2n.word_to_num", return_value=50):
            response = player.set_volume(String("пятьдесят"))
    
        mock_run.assert_called_with(["amixer", "sset", "Master", "50%"])  # Исправили general_player на mock_run
        assert response is None  # Метод не должен возвращать ошибку

    @patch("subprocess.run")
    def test_maximum(self, mock_run, general_player):  # Добавили mock_run
        player = general_player
        player.maximum()
        mock_run.assert_called_with(["amixer", "sset", "Master", "100%"])

    @patch("subprocess.run")
    def test_minimum(self, mock_run, general_player):  # Добавили mock_run
        player = general_player
        player.minimum()
        mock_run.assert_called_with(["amixer", "sset", "Master", "20%"])

    @patch("subprocess.run")
    def test_turn_off_the_sound(self, mock_run, general_player):  # Добавили mock_run
        player = general_player
        player.turn_off_the_sound()
        mock_run.assert_called_with(["amixer", "sset", "Master", "0%"])