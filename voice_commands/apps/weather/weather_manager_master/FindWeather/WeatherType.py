from enum import Enum

sun_codes = [1000]


lit_precip_codes = [
    1063,
    1066,
    1072,
    1135,
    1150,
    1153,
    1180,
    1183,
    1189,
    1186,
    1198,
    1210,
    1213,
    1216,
    1219,
    1240,
    1255,
    1261,
]


strong_precip_codes = [
    1114,
    1117,
    1168,
    1147,
    1171,
    1192,
    1195,
    1201,
    1207,
    1222,
    1225,
    1237,
    1243,
    1246,
    1252,
    1258,
]


thunder_codes = [1087, 1273, 1276, 1279, 1282]


cloudy_codes = [1003, 1006, 1009, 1030]


sleet_codes = [1000, 1003, 1006]


# zombie_codes = []


# radio_codes = []


class WeatherType(str, Enum):
    sun = "Хорошая погода"

    lit_precip = "Слабые осадки, возможно туман или снежок"

    strong_precip = "Сильные осадки"

    cloudy = "Облачно"

    thunder = "Гром"

    sleet = "Опасно, скользко!"

    windy = "Очень сильный ветер"

    # zombie = 'ГОТОВЬ ОРУЖИЕ И ИДИ В БУНКЕР'

    # radio = 'ГОТОВЬ СЧЕТЧИК ГЕЙГЕРА И ИДИ В БУНКЕР'

    @staticmethod
    def get_type_by_code(code: int) -> str | None:
        if code in sun_codes:
            return WeatherType.sun

        elif code in lit_precip_codes:
            return WeatherType.lit_precip

        elif code in strong_precip_codes:
            return WeatherType.strong_precip

        elif code in cloudy_codes:
            return WeatherType.cloudy

        elif code in sleet_codes:
            return WeatherType.sleet

        elif code in thunder_codes:
            return WeatherType.thunder
        else:
            return None
