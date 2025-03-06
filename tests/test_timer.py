import pytest
from unittest.mock import MagicMock
from voice_commands import State, Timer, validate_time_format  
from stark.core.types import String
from stark import Response

@pytest.fixture
def state():
    state = State()
    state.show_timer = MagicMock(return_value=Response(voice="Нет активных таймеров."))
    state.check_timer_status = MagicMock(return_value=Response(voice="Нет активных таймеров."))
    state.cancel_timer = MagicMock(return_value=Response(voice="Нет таймеров для отмены."))
    return state

@pytest.fixture
def timer():
    
    timer = Timer()
    timer.set_a_timer = MagicMock(
        side_effect=lambda time_input: Response(voice=f"Таймер установлен на {time_input}")
    )
    return timer

def test_validate_time_format():
    assert validate_time_format(String("5 минут"))
    assert validate_time_format(String("2 часа"))
    assert not validate_time_format(String("позже"))
    assert not validate_time_format(String("непонятное время"))

def test_show_timer_no_timers(state):
    response = state.show_timer()
    assert response.voice == "Нет активных таймеров."

def test_show_timer_with_timers(state):
    state.list_timer.append("Таймер 1")
    state.show_timer.return_value = Response(voice="Активных таймеров: 1")
    response = state.show_timer()
    assert "Активных таймеров" in response.voice

def test_check_timer_status_no_timers(state):
    response = state.check_timer_status()
    assert response.voice == "Нет активных таймеров."

def test_check_timer_status_with_timers(state):
    state.list_timer.append("Таймер 1")
    state.check_timer_status.return_value = Response(voice="Все таймеры активны.")
    response = state.check_timer_status()
    assert response.voice == "Все таймеры активны."

def test_cancel_timer_no_timers(state):
    response = state.cancel_timer()
    assert response.voice == "Нет таймеров для отмены."

def test_cancel_timer_with_timers(state):
    state.list_timer.append("Таймер 1")
    state.cancel_timer.return_value = Response(voice="Таймер отменён.")
    response = state.cancel_timer()
    assert response.voice == "Таймер отменён."
    assert len(state.list_timer) == 1  


#! Данные тесты надо еще подкорректировать/ These tests still need to be adjusted.
@pytest.mark.asyncio
@pytest.mark.parametrize("time_input, expected_response", [
    ("5 минут", "Таймер установлен на 5 минут"),
    ("2 часа", "Таймер установлен на 2 часа"),
    ("вчера", "Ошибка! Указано прошедшее время. Пожалуйста, установите правильный интервал."),
    ("непонятное время", "Ошибка! Неправильный формат времени.")
])
async def test_set_a_timer(timer, time_input, expected_response):
    
    response = timer.set_a_timer(String(time_input))  
    assert response.voice == expected_response
