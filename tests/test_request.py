import pytest
from unittest.mock import patch, MagicMock
from stark.core.types import String
from voice_commands import Request  
import pywhatkit
from pywhatkit.core.exceptions import InternetException

# Тесты проверяют функционал, а также производится проверка на наличие интернета
def test_is_connect_success():
    with patch("socket.create_connection", return_value=True):
        assert Request.is_connect() is True

def test_is_connect_failure():
    with patch("socket.create_connection", side_effect=OSError):
        assert Request.is_connect() is False

def test_find_the_answer_no_internet():
    request = Request()
    with patch.object(Request, "is_connect", return_value=False):
        response = request.find_the_answer(String("Что такое Python?"))
    assert response.voice == "Ответ не найден, или же отсутствует соединение"

def test_find_the_answer_success():
    request = Request()
    with patch.object(Request, "is_connect", return_value=True), \
         patch("pywhatkit.search", return_value=None) as mock_search:
        response = request.find_the_answer(String("Что такое Python?"))
    mock_search.assert_called_once_with("Что такое Python?")
    assert response.voice == "Выполняю запрос"

def test_find_the_answer_internet_exception():
    request = Request()
    with patch.object(Request, "is_connect", return_value=True), \
         patch("pywhatkit.search", side_effect=InternetException):
        response = request.find_the_answer(String("Что такое Python?"))
    assert response.voice == "Ошибка сети: не удалось выполнить запрос, но работа продолжается."

def test_find_the_answer_unexpected_exception():
    request = Request()
    with patch.object(Request, "is_connect", return_value=True), \
         patch("pywhatkit.search", side_effect=Exception("Some error")):
        response = request.find_the_answer(String("Что такое Python?"))
    assert "Произошла ошибка" in response.voice
