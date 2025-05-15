from FindWeather.WeatherManager import WeatherManager
from pprint import pprint

API_KEY = "6529245dc1ac4297849161313250105"
CITY = "Москва"

url = "https://api.weatherapi.com/v1/current.json"

wm = WeatherManager(api_key=API_KEY, place_code=CITY, days_count=3)

# Получить текущую погоду
current = wm.get_current()

# Если ошибка, то выводим ошибку
if not current:
    print("Ошибка получения текущей погоды")
else:
    print("Текущая погода:")
    pprint(current.__dict__)

# Получить прогноз на несколько дней
days = wm.get_days()
print("\nПрогноз на дни:")
if days:
    for day in days:
        print(f"{day.date.strftime('%d.%m.%Y')}: {day.temp_c}°C, {day.condition_text}")
else:
    print("Ошибка получения прогноза")