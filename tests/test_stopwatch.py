import pytest
from voice_commands import Stopwatch

@pytest.mark.anyio
async def test_start_stopwatch(mocker):
    mocker.patch("anyio.sleep", return_value=None)
    stopwatch = Stopwatch()
    responses = []
    async for resp in stopwatch.start():
        responses.append(resp)
        break  # Прерываем цикл, чтобы тест не длился бесконечно
    assert "Секундомер запущен" in responses[0].voice
    assert stopwatch.running is True

@pytest.mark.anyio
async def test_start_stopwatch_already_running():
    stopwatch = Stopwatch()
    stopwatch.running = True
    responses = []
    async for resp in stopwatch.start():
        responses.append(resp)
    assert "Секундомер уже работает" in responses[0].voice

@pytest.mark.anyio
async def test_stop_stopwatch():
    stopwatch = Stopwatch()
    stopwatch.running = True
    stopwatch.seconds = 5
    responses = []
    async for resp in stopwatch.stop():
        responses.append(resp)
    assert "Секундомер остановлен" in responses[0].voice
    assert "пятьой" in responses[0].voice  # Проверяем просто число
    assert stopwatch.running is False

@pytest.mark.anyio
async def test_stop_stopwatch_already_stopped():
    stopwatch = Stopwatch()
    responses = []
    async for resp in stopwatch.stop():
        responses.append(resp)
    assert "Секундомер уже остановлен" in responses[0].voice
    assert stopwatch.running is False

@pytest.mark.anyio
async def test_reset_stopwatch():
    stopwatch = Stopwatch()
    stopwatch.running = True
    stopwatch.seconds = 10
    responses = []
    async for resp in stopwatch.reset():
        responses.append(resp)

    assert "\nСекундомер остановлен на десятьой секунде" in responses[0].voice
    assert stopwatch.seconds == 0
    assert stopwatch.running is False

@pytest.mark.anyio
async def test_reset_stopwatch_not_running():
    stopwatch = Stopwatch()
    responses = []
    async for resp in stopwatch.reset():
        responses.append(resp)
    print(responses[0].voice)
    assert "Секундомер сброшен" in responses[0].voice
    assert stopwatch.seconds == 0
    assert stopwatch.running is False
