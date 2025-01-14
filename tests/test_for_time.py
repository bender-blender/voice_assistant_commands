import unittest
from datetime import datetime
from voice_commands import get_the_day, get_time, convert


class TestVoiceAssistant(unittest.TestCase):

    async def test_get_the_day(self):
        """Проверяет, что функция возвращает корректную дату."""
        response = await get_the_day()
        today = datetime.now()
        # Проверяем, что текущий день, месяц и год присутствуют в ответе
        self.assertIn(str(today.day), response.voice)
        self.assertIn(str(today.month), response.voice)
        self.assertIn(str(today.year), response.voice)

    async def test_get_time(self):
        """Проверяет, что функция возвращает корректное время."""
        response = await get_time()
        now = datetime.now()
        # Проверяем, что текущие часы и минуты присутствуют в ответе
        self.assertIn(str(now.hour), response.voice)
        self.assertIn(str(now.minute), response.voice)

    def test_convert(self):
        """Проверяет преобразование чисел в слова."""
        self.assertEqual(convert(1), "один")
        self.assertEqual(convert(21), "двадцать один")
        self.assertEqual(convert(2023), "две тысячи двадцать три")


if __name__ == "__main__":
    unittest.main()
