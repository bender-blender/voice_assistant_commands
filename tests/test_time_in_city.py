import pytest
from unittest.mock import patch
from voice_commands.clock.providers import TimeCityProvider
from voice_commands.models.model_time import TimeModel
from stark import Response

@pytest.mark.parametrize("city,coords", [
    ("Москва", (55.7558, 37.6173)),
    ("Нью-Йорк", (40.7128, -74.0060)),
    ("Токио", (35.6895, 139.6917)),
    ("Лондон", (51.5074, -0.1278)),
    ("Сидней", (-33.8688, 151.2093)),
    ("Берлин", (52.52, 13.405)),
    ("Париж", (48.8566, 2.3522)),
    ("Рим", (41.9028, 12.4964)),
    ("Пекин", (39.9042, 116.4074)),
    ("Торонто", (43.651070, -79.347015)),
])
def test_get_time_by_city_mocked(city, coords):
    with patch("voice_commands.models.model_city.CityInfo.get_coordinates", return_value=coords):
        provider = TimeCityProvider(city)
        result = provider.get_time_by_coordinates()
        assert isinstance(result, TimeModel)

@pytest.mark.parametrize("invalid_city", [
    "",              
    "НеГород123",    
    "!!!",           
    None,            
])
def test_get_time_by_city_invalid_params(invalid_city):
    with patch("voice_commands.models.model_city.CityInfo.get_coordinates", return_value=None):
        provider = TimeCityProvider(invalid_city)
        result = provider.get_time_by_coordinates()
        assert result is None or isinstance(result, Response)  


@pytest.mark.parametrize("country,coords", [
    ("Россия", (55.751244, 37.618423)),
    ("США", (38.89511, -77.03637)),
    ("Япония", (35.682839, 139.759455)),
    ("Франция", (48.8566, 2.3522)),
    ("Бразилия", (-15.793889, -47.882778)),
])
def test_get_time_by_country_mocked(country, coords):
    with patch("voice_commands.models.model_city.CityInfo.get_coordinates", return_value=coords):
        provider = TimeCityProvider(country)
        result = provider.get_time_by_coordinates()
        assert isinstance(result, TimeModel)

@pytest.mark.parametrize("invalid_country", [
    "",             
    "НеСтрана456",  
    "???",          
    None,           
])
def test_get_time_by_country_invalid_params(invalid_country):
    with patch("voice_commands.models.model_city.CityInfo.get_coordinates", return_value=None):
        provider = TimeCityProvider(invalid_country)
        result = provider.get_time_by_coordinates()
        
        assert result is None or isinstance(result, Response)
