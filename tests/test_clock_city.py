import pytest
from unittest.mock import patch, MagicMock
from stark import Response
from voice_commands import get_current_time_in_city
from dependencies.auxiliary_functions import convert

@pytest.fixture
def mock_geolocator():
    with patch("voice_commands.clock.time_in_another_city.Nominatim") as mock:
        yield mock

@pytest.fixture
def mock_timezone_finder():
    with patch("voice_commands.clock.time_in_another_city.TimezoneFinder") as mock:
        yield mock

@pytest.fixture
def mock_convert():
    with patch("dependencies.auxiliary_functions.convert") as mock:
        yield mock

# Параметризация для 20 городов
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "city, lat, lon, timezone",
    [
        ("Москва", 55.7558, 37.6173, "Europe/Moscow"),
        ("Лондон", 51.5074, -0.1278, "Europe/London"),
        ("Нью-Йорк", 40.7128, -74.0060, "America/New_York"),
        ("Париж", 48.8566, 2.3522, "Europe/Paris"),
        ("Берлин", 52.5200, 13.4050, "Europe/Berlin"),
        ("Токио", 35.6895, 139.6917, "Asia/Tokyo"),
        ("Сидней", -33.8688, 151.2093, "Australia/Sydney"),
        ("Рио-де-Жанейро", -22.9068, -43.1729, "America/Sao_Paulo"),
        ("Каир", 30.0444, 31.2357, "Africa/Cairo"),
        ("Дубай", 25.276987, 55.296249, "Asia/Dubai"),
        ("Пекин", 39.9042, 116.4074, "Asia/Shanghai"),
        ("Сингапур", 1.3521, 103.8198, "Asia/Singapore"),
        ("Мадрид", 40.4168, -3.7038, "Europe/Madrid"),
        ("Рим", 41.9028, 12.4964, "Europe/Rome"),
        ("Амстердам", 52.3676, 4.9041, "Europe/Amsterdam"),
        ("Сеул", 37.5665, 126.9780, "Asia/Seoul"),
        ("Стамбул", 41.0082, 28.9784, "Europe/Istanbul"),
        ("Дели", 28.7041, 77.1025, "Asia/Kolkata"),
        ("Торонто", 43.65107, -79.347015, "America/Toronto"),
        ("Кейптаун", -33.9249, 18.4241, "Africa/Johannesburg"),
    ],
)
async def test_city_time(mock_geolocator, mock_timezone_finder, mock_convert, city, lat, lon, timezone):
    # Настраиваем мок для геолокатора
    mock_geolocator.return_value.geocode.return_value = MagicMock(latitude=lat, longitude=lon)

    # Настраиваем мок для временной зоны
    mock_timezone_finder.return_value.timezone_at.return_value = timezone

    # Настраиваем функцию `convert`
    mock_convert.side_effect = lambda x: str(x)

    # Проверяем конкретный город
    response = await get_current_time_in_city(city=MagicMock(value=city))
    assert isinstance(response, Response)
    assert f"Текущее время в {city}" in response.voice

@pytest.mark.asyncio
async def test_city_not_found(mock_geolocator):
    # Настраиваем случай, когда город не найден
    mock_geolocator.return_value.geocode.return_value = None

    # Проверяем несуществующий город
    response = await get_current_time_in_city(city=MagicMock(value="НесуществующийГород"))
    assert isinstance(response, Response)
    assert response.voice == "Город НесуществующийГород не найден"
