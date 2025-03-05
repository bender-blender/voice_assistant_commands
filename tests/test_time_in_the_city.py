import pytest
from voice_commands import CityTime
from stark.core.types import String
from unittest.mock import MagicMock

@pytest.fixture
def prepare_cities():
    city_time = CityTime()
    
    # Мокаем метод get_time_in_city для разных городов
    def mock_get_time_in_city(city):
        mock_response = MagicMock()
        mock_response.voice = city.value  # Возвращаем название города как часть voice
        return mock_response
    
    city_time.get_time_in_city = mock_get_time_in_city
    return city_time



@pytest.mark.parametrize("city",
                        (
                        String("Москва"), String("Токио"), String("Париж"),
                        String("Нью-Йорк"), String("Барселона"), String("Лондон"),
                        String("Сидней"), String("Берлин"), String("Рим"),
                        String("Стамбул"), String("Амстердам"), String("Дубай"),
                        String("Сан-Франциско"), String("Сингапур"), String("Шанхай"),
                        String("Гонконг"), String("Мадрид"), String("Лос-Анджелес"),
                        String("Торонто"), String("Мехико"), String("Буэнос-Айрес"),
                        String("Сан-Паулу"), String("Мумбаи"), String("Каир"),
                        String("Кейптаун"), String("Сеул"), String("Осака"),
                        String("Вена"), String("Бангкок"), String("Прага")))

def test_city_time(city,prepare_cities):
    object_city = prepare_cities
    
    response = object_city.get_time_in_city(city)

    assert response.voice is not None
    print(response.voice)
    assert city.value in response.voice

#pytest -s tests/test_time_in_the_city.py 