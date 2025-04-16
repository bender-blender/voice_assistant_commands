import os
import pytest
from datetime import datetime
from voice_commands.note.notes import Note
from stark import Response

# Моки типов
class MockString:
    def __init__(self, value):
        self.value = value

class MockTime:
    def __init__(self, day):
        self.day = day

class MockYear:
    def __init__(self, year):
        self.year = year

class MockHours:
    def __init__(self, hour):
        self.hour = hour


@pytest.fixture
def note():
    return Note()


def test_create_note(note):
    response = note.create_a_note()
    assert response.voice == "Заметка создана"

def test_create_note_twice(note):
    note.create_a_note()
    response = note.create_a_note()
    assert "уже создана" in response.voice

def test_add_summary(note):
    note.create_a_note()
    response = note.add_summary(MockString("Обсудить стратегию"))
    assert response.voice == "Описание добавлено"
    assert note.event_summary == "Обсудить стратегию"

def test_add_summary_twice(note):
    note.create_a_note()
    note.add_summary(MockString("Первое"))
    response = note.add_summary(MockString("Второе"))
    assert "уже добавлено" in response.voice

def test_add_time(note):
    note.create_a_note()
    response = note.add_time(MockTime("3 марта"))
    assert response.voice == "Дата добавлена"
    assert note.event_date == "3 марта"

def test_add_time_twice(note):
    note.create_a_note()
    note.add_time(MockTime("3 марта"))
    response = note.add_time(MockTime("4 марта"))
    assert "уже добавлена" in response.voice

def test_add_year(note):
    note.create_a_note()
    response = note.add_year(MockYear(2026))
    assert response.voice == "Год добавлен"
    assert note.event_year == 2026

def test_add_year_twice(note):
    note.create_a_note()
    note.add_year(MockYear(2026))
    response = note.add_year(MockYear(2027))
    assert "уже добавлен" in response.voice

def test_add_time_and_save(tmp_path):
    os.chdir(tmp_path)
    note = Note()
    note.create_a_note()
    note.add_summary(MockString("Тест"))
    note.add_time(MockTime("2 февраля"))
    note.start_date(MockHours("12:00"))
    note.add_year(MockYear(2025))

    response = note.save_event()
    assert "успешно" in response.voice
    assert os.path.exists("events.ics")
    assert len(note.events) == 1

def test_save_event_missing_fields(note):
    note.create_a_note()
    note.add_summary(MockString("Без даты и времени"))
    response = note.save_event()
    assert "Заполните описание, дату и время" in response.voice

def test_add_location(note):
    note.create_a_note()
    response = note.add_location(MockString("Москва"))
    assert response.voice == "Локация добавлена"
    assert note.event_location == "Москва"

def test_add_location_twice(note):
    note.create_a_note()
    note.add_location(MockString("Москва"))
    response = note.add_location(MockString("Санкт-Петербург"))
    assert "Локация добавлена" in response.voice

def test_save_event_error_handling(monkeypatch):
    note = Note()
    note.create_a_note()
    note.add_summary(MockString("Ошибка сохранения"))
    note.add_time(MockTime("3 марта"))
    note.start_date(MockHours("12:00"))
    note.add_year(MockYear(2025))

    # Ломаем dateparser
    monkeypatch.setattr("voice_commands.note.notes.dateparser.parse", lambda x: (_ for _ in ()).throw(ValueError("тестовая ошибка")))

    response = note.save_event()
    assert "Ошибка при сохранении события" in response.voice