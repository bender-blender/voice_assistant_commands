import pytest
import asyncio
from stark import Response, CommandsManager

# Импортируем ваш код секундомера (предполагается, что он находится в файле stopwatch.py)
from voice_commands import stopwatch, elapsed_time, running

@pytest.mark.asyncio
async def test_start_timer():
    global running, elapsed_time  # Добавляем глобальные переменные для доступа к состоянию
    # Проверяем начальное состояние
    assert not running
    assert elapsed_time == 0

    # Запускаем таймер
    await stopwatch.commands[0]()  # Предполагаем, что команда 'старт' - первая в списке
    
    # Ждем несколько секунд, чтобы таймер мог обновиться
    await asyncio.sleep(2)
    
    # Проверяем состояние после запуска
    assert running
    assert elapsed_time >= 2  # Прошедшее время должно быть больше или равно 2 секундам

@pytest.mark.asyncio
async def test_stop_timer():
    global running, elapsed_time  # Добавляем глобальные переменные для доступа к состоянию
    # Сначала запускаем таймер
    await stopwatch.commands[0]()  # Запускаем 'старт'
    
    # Ждем немного времени
    await asyncio.sleep(1)
    
    # Останавливаем таймер
    response = await stopwatch.commands[1]()  # Предполагаем, что команда 'стоп' - вторая в списке
    
    # Проверяем состояние после остановки
    assert not running
    assert response.text.startswith("Секундомер остановлен.")
    assert elapsed_time >= 1  # Прошедшее время должно быть больше или равно 1 секунде

@pytest.mark.asyncio
async def test_reset_timer():
    global running, elapsed_time  # Добавляем глобальные переменные для доступа к состоянию
    # Запускаем таймер
    await stopwatch.commands[0]()  # Запускаем 'старт'
    
    # Ждем немного времени
    await asyncio.sleep(1)
    
    # Сбрасываем таймер
    response = await stopwatch.commands[2]()  # Предполагаем, что команда 'сброс' - третья в списке
    
    # Проверяем состояние после сброса
    assert elapsed_time == 0
    assert not running
    assert response.text == "Секундомер сброшен."