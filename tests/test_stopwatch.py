import pytest
from voice_commands.stopwatch.providers.provider_stopwatch import Stopwatch
import time

def test_start_sets_start_time(monkeypatch):
    fake_time = 123456.789
    monkeypatch.setattr("time.time", lambda: fake_time)
    
    sw = Stopwatch()
    sw.start()
    
    assert sw.start_time == fake_time

def test_elapsed_returns_correct_time(monkeypatch):
    sw = Stopwatch()
    
    # Симулируем время старта
    start_time = 100.0
    monkeypatch.setattr("time.time", lambda: start_time)
    sw.start()

    # Симулируем текущее время
    monkeypatch.setattr("time.time", lambda: start_time + 2.5)
    elapsed = sw.elapsed()
    
    assert elapsed == pytest.approx(2.5, abs=0.01)

def test_elapsed_raises_without_start():
    sw = Stopwatch()
    with pytest.raises(TypeError, match="unsupported operand type"):
        sw.elapsed()