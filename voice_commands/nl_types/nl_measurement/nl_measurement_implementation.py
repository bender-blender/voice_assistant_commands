from pymorphy3 import MorphAnalyzer
from pint import UnitRegistry


from .nl_measurement_interface import MeasurementParseInterface
from .units import ureg



class MeasurementParseRu(MeasurementParseInterface):

    def __init__(self) -> None:
        super().__init__() 
        self.pint = ureg

        self.dictionary_quantities = {

            "фут": self.pint.foot,
            "метр": self.pint.meter,
            "миля": self.pint.mile,
            "километр": self.pint.kilometer,


            "грамм": self.pint.gram,
            "килограмм": self.pint.kilogram,
            "фунт": self.pint.pound,
            "унция": self.pint.ounce,


            "секунда": self.pint.second,
            "минута": self.pint.minute,
            "час": self.pint.hour,


            "цельсий": self.pint.degC,
            "фаренгейт": self.pint.degF,
            "кельвин": self.pint.kelvin,


            "метр в секунду": self.pint.meter / self.pint.second,
            "километр в час": self.pint.kilometer / self.pint.hour,
            "миля в час": self.pint.mile / self.pint.hour,


            "литр": self.pint.liter,
            "миллилитр": self.pint.milliliter,
            "чашка": self.pint.cup,
            "галлон": self.pint.gallon,


            "джоуль": self.pint.joule,
            "калория": self.pint.calorie,
            "киловатт час": self.pint.kilowatt_hour,


            "ватт": self.pint.watt,
            "киловатт": self.pint.kilowatt,
        }
    
    def parse(self, from_string: str) -> UnitRegistry | None:
        split_line = from_string.lower().split()
        morphy = MorphAnalyzer()
        result = [
            self.dictionary_quantities[morphy.parse(value)[0].normal_form] for value in split_line
            if morphy.parse(value)[0].normal_form in self.dictionary_quantities
            ]

        if result:
            return result[0]

        return None



class MeasurementParseEn(MeasurementParseInterface):

    def __init__(self) -> None:
        super().__init__()
        self.pint = ureg
        self.dictionary_quantities = {
            "foot": self.pint.foot,
            "feet": self.pint.foot,
            "metre": self.pint.meter,
            "metres": self.pint.meter,
            "meter": self.pint.meter,
            "meters": self.pint.meter,
            "mile": self.pint.mile,
            "miles": self.pint.mile,
            "kilometre": self.pint.kilometer,
            "kilometres": self.pint.kilometer,

            "gram": self.pint.gram,
            "grams": self.pint.gram,
            "kilogram": self.pint.kilogram,
            "kilograms": self.pint.kilogram,
            "pound": self.pint.pound,
            "pounds": self.pint.pound,
            "ounce": self.pint.ounce,
            "ounces": self.pint.ounce,

            "second": self.pint.second,
            "seconds": self.pint.second,
            "minute": self.pint.minute,
            "minutes": self.pint.minute,
            "hour": self.pint.hour,
            "hours": self.pint.hour,

            "celsius": self.pint.degC,
            "fahrenheit": self.pint.degF,
            "kelvin": self.pint.kelvin,

            "metre per second": self.pint.meter / self.pint.second,
            "metres per second": self.pint.meter / self.pint.second,
            "kilometre per hour": self.pint.kilometer / self.pint.hour,
            "kilometres per hour": self.pint.kilometer / self.pint.hour,
            "mile per hour": self.pint.mile / self.pint.hour,
            "miles per hour": self.pint.mile / self.pint.hour,
            "mph": self.pint.mile / self.pint.hour,

            "litre": self.pint.liter,
            "litres": self.pint.liter,
            "liter": self.pint.liter,
            "liters": self.pint.liter,


            "millilitre": self.pint.milliliter,
            "millilitres": self.pint.milliliter,
            "cup": self.pint.cup,
            "cups": self.pint.cup,
            "gallon": self.pint.gallon,
            "gallons": self.pint.gallon,

            "joule": self.pint.joule,
            "joules": self.pint.joule,
            "calorie": self.pint.calorie,
            "calories": self.pint.calorie,
            "kilowatt hour": self.pint.kilowatt_hour,
            "kilowatt hours": self.pint.kilowatt_hour,
            "kwh": self.pint.kilowatt_hour,

            "watt": self.pint.watt,
            "watts": self.pint.watt,
            "kilowatt": self.pint.kilowatt,
            "kilowatts": self.pint.kilowatt,
        }
    
    def parse(self, from_string: str) -> UnitRegistry | None:
        split_line = from_string.lower().split()
        result = [
            self.dictionary_quantities[value] for value in split_line
            if value in self.dictionary_quantities
        ]

        if result:
            return result[0]

        return None
