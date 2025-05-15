import logging
from FindWeather.WeatherManager import WeatherManager
from aiogram import Bot, Dispatcher, executor, types


# TODO: All api keys to config.py or .env (.env better)
# TODO: Create MessageFormatter.py with functions for creating text messages
#       (move creating f-strings to separate file)

API_TOKEN = '5380449281:AAFEWSaGhkEtNGmzv0f0u6xV_W_Mn6qhIus'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
   await message.answer("Hi!\nI'm WeatherManagerBot!")

@dp.message_handler(commands=['current'])
async def current_weather(message: types.Message):
    manager = WeatherManager('f4a07d9c0d484fc8b7491537221405', 'port-imeni-lenina-2515498')
    current = manager.get_current()
    msg_text = f'''Сейчас {current.weather_type.lower()}
Температура: {current.temp_c} °C'''
    await message.answer(msg_text)

@dp.message_handler(commands=['day1', 'today'])
async def days_weather(message: types.Message):
    manager = WeatherManager('f4a07d9c0d484fc8b7491537221405', 'port-imeni-lenina-2515498')
    days = manager.get_days()
    # TODO: parse date from message.text and choose day by date,
    #       return error message if day with date not found
    day1 = days[0]
    msg_text = f'''{day1.date.strftime('%d.%m')} будет {day1.weather_type.lower()}
Средняя температура: {day1.temp_c} °C'''
    await message.answer(msg_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
