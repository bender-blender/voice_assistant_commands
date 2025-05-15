import pytest
from unittest.mock import patch
from datetime import datetime
from stark import Response
from dependencies.helpers import convert
from voice_commands import Time  # Замените your_module на реальное имя файла

@pytest.fixture
def time_instance():
    return Time()

@patch('voice_commands.clock.current_time.datetime')  # Мокаем datetime
@patch('voice_commands.clock.current_time.convert', side_effect=lambda x: str(x))  # Мокаем convert
def test_show_time(mock_convert, mock_datetime, time_instance):
    mock_datetime.now.return_value = datetime.now()
    response = time_instance.show_time()
    
    current_time = datetime.now()
    expected_text = f"Сейчас {current_time.hour} часов {current_time.minute} минут"
    
    assert isinstance(response, Response)
    assert response.voice == expected_text

@patch.object(Time, 'show_time')
def test_voice_response(mock_show_time, time_instance):
    mock_show_time.return_value = Response(voice="Сейчас X часов Y минут")
    response = time_instance.show_time()
    
    assert "Сейчас" in response.voice
    assert "часов" in response.voice
    assert "минут" in response.voice
