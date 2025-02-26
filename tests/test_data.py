import pytest
from datetime import datetime
from voice_commands import Data  # Импортируйте ваш модуль, где находится класс Data
from stark import CommandsManager, Response


class MockRecognizer:
    """Заглушка для распознавания речи."""
    def recognize(self):
        return "какое сегодня число?"  # Симулируем распознавание запроса


class MockSynthesizer:
    """Заглушка для синтезатора речи."""
    def synthesize(self, text: str):
        return f"Синтезированный голос: {text}"  # Симулируем синтез речи


@pytest.fixture
def data_instance():
    """Фикстура для создания экземпляра Data"""
    return Data()  # Инициализация объекта Data


@pytest.fixture
def mock_recognizer():
    """Фикстура для создания MockRecognizer"""
    return MockRecognizer()


@pytest.fixture
def mock_synthesizer():
    """Фикстура для создания MockSynthesizer"""
    return MockSynthesizer()


def test_voice_interaction(data_instance, mock_recognizer, mock_synthesizer):
    # Получаем текущее время
    now = datetime.now()

    # Симуляция распознавания голоса
    recognized_text = mock_recognizer.recognize()
    assert recognized_text == "какое сегодня число?"  # Проверяем, что запрос правильно распознан

    # Сгенерированный ответ
    response_text = f"Сегодня {now.day} день {now.hour} час {now.minute} минута"
    
    # Симулируем работу синтезатора речи
    response_voice = mock_synthesizer.synthesize(response_text)
    
    # Проверяем, что синтезированный голос соответствует ожидаемому ответу
    assert response_voice == f"Синтезированный голос: {response_text}"

    # Запускаем команду, которая должна вернуть правильный текст
    response = data_instance.show_date()

    # Проверяем, что результат синтезированного голоса от Data соответствует ожидаемому
    assert response.voice == f"Сегодня {now.day} день {now.hour} час {now.minute} минута"