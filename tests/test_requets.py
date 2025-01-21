import pytest
from unittest.mock import patch
import pywhatkit as kit
from voice_commands import is_connected, answer  # Замените на актуальное имя модуля


# Тест для функции проверки наличия интернета
@pytest.mark.asyncio
@patch('socket.create_connection')
async def test_is_connected_success(mock_create_connection):
    mock_create_connection.return_value = True
    assert is_connected() is True  # Убираем await, так как is_connected синхронная


@pytest.mark.asyncio
@patch('socket.create_connection')
async def test_is_connected_failure(mock_create_connection):
    mock_create_connection.side_effect = OSError
    assert is_connected() is False  # Убираем await, так как is_connected синхронная


# Тест для команды ответа с доступом в интернет
@pytest.mark.asyncio
@patch('pywhatkit.search')
@patch('voice_commands.is_connected')  # Патчим функцию is_connected для симуляции доступности интернета
async def test_answer_with_internet(mock_is_connected, mock_search):
    mock_is_connected.return_value = True  # Интернет доступен
    mock_search.return_value = None  # Симулируем успешный вызов pywhatkit.search

    query = {"query": "Как дела?"}  # Оборачиваем строку в словарь
    response = await answer(query)  # Используем await для асинхронной функции

    # Проверяем, что ответ соответствует ожидаемому
    assert response.voice == "Отрабатываю запрос"


# Тест для команды ответа без интернета
@pytest.mark.asyncio
@patch('voice_commands.is_connected')
async def test_answer_without_internet(mock_is_connected):
    mock_is_connected.return_value = False  # Интернет недоступен

    query = {"query": "Как дела?"}  # Оборачиваем строку в словарь
    response = await answer(query)  # Используем await для асинхронной функции

    # Проверяем, что ответ об отсутствии интернета правильный
    assert response.voice == "Нет подключения к интернету. Пожалуйста, проверьте соединение."


# Тест для команды ответа с ошибкой поиска
@pytest.mark.asyncio
@patch('pywhatkit.search')
@patch('voice_commands.is_connected')
async def test_answer_with_search_error(mock_is_connected, mock_search):
    mock_is_connected.return_value = True  # Интернет доступен
    mock_search.side_effect = Exception("Search error")  # Симулируем ошибку при поиске

    query = {"query": "Как дела?"}  # Оборачиваем строку в словарь
    response = await answer(query)  # Используем await для асинхронной функции

    # Проверяем, что ответ об ошибке правильный
    assert response.voice == "Ошибка, попробуйте еще раз"
