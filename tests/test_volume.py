import unittest
from voice_commands.apps.mediaplayer.parameters.volume import Volume


class TestValue(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.volume = Volume(None)

    async def test_set_volume(self):
        list_phrases = [
            "Громкость пятьдесят девять",
            "Громкость сорок девять",
            "Громкость один",
            "Громкость двадцать восемь",
        ]

        result = ["59", "49", "1", "28"]
        for pharase, volume in zip(list_phrases, result):
            res = await self.volume.did_parse(pharase)
            print(res)
            self.assertEqual(res, volume)


if __name__ == "__main__":
    unittest.main()
