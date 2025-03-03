import pytest
from datetime import datetime
from voice_commands import Data, data_manager
from dependencies import convert


@pytest.fixture
def data_instance():
    """Фикстура для создания экземпляра Data"""
    return Data()  # Инициализация объекта Data


@pytest.fixture
def phrase_templates(): # Фикстура для шаблона фраз
    patterns = [
    p.lstrip("(").rstrip(")") 
    for command in data_manager.commands 
    for p in str(command.pattern).lstrip("<Pattern '").rstrip("'>").split("|")
    ]
    return patterns

def test_voice_interaction(data_instance,phrase_templates):

    phrase = [
            "какое сегодня число",
            "какой сегодня день", "какая сегодня дата"]
    
    # Получаем текущее время
    months = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    time = datetime.now()
    day = time.day
    month = time.month
    year = time.year

    for phrases in phrase:
        
        assert phrases in phrase_templates
        data = data_instance.show_date()
        assert data.voice == f"Сегодня {convert(day)} {months[month-1]} {convert(year)} года"

