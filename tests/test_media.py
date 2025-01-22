import pytest
from voice_commands import play, pause, next_track, previous_track, set_volume, get_info
import asyncio

@pytest.mark.asyncio
async def test_play():
    try:
        await play()
        assert True
    except Exception as e:
        pytest.fail(f"Функция play вызвала ошибку: {e}")

@pytest.mark.asyncio
async def test_pause():
    try:
        await pause()
        assert True
    except Exception as e:
        pytest.fail(f"Функция pause вызвала ошибку: {e}")

@pytest.mark.asyncio
async def test_next_track():
    try:
        await next_track()
        assert True
    except Exception as e:
        pytest.fail(f"Функция next_track вызвала ошибку: {e}")

@pytest.mark.asyncio
async def test_previous_track():
    try:
        await previous_track()
        assert True
    except Exception as e:
        pytest.fail(f"Функция previous_track вызвала ошибку: {e}")

@pytest.mark.asyncio
async def test_set_volume():
    try:
        await set_volume({"vol1": 50})  # Передаем параметр как словарь
        assert True
    except Exception as e:
        pytest.fail(f"Функция set_volume вызвала ошибку: {e}")



