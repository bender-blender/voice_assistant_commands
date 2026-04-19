from pint import UnitRegistry

from voice_commands.nl_types.nl_measurement.nl_measurement import NLMeasurement
from voice_commands.nl_types.nl_measurement.nl_unit import NLAbstractUnit
from voice_commands.nl_types.parsing_context import pattern_parser
from voice_commands.nl_types.nl_measurement.nl_group import Group
from voice_commands.nl_types.nl_measurement.generation_pattern import create_pattern
from locales.variables import translator


unit = UnitRegistry()



ru_word = [
    "километр*",
    "метр*",
    "миля*",
    "фут*",
    "грамм*",
    "килограмм*",
    "фунт*",
    "унци*",
    "секунд*",
    "минут*",
    "час*",
    "градус*",
    "цельси*",
    "фаренгейт*",
    "кельвин*",
    "метр* в секунд*",
    "километр* в час*",
    "мил* в час*",
    "литр*",
    "миллилитр*",
    "чашк*",
    "галлон*",
    "джоул*",
    "калори*",
    "киловатт* час*",
    "ватт*",
    "киловатт*",
    "градус*",
]


en_word = [
    "kilometer*",
    "meter*",
    "mile*",
    "foot*",
    "gram*",
    "kilogram*",
    "pound*",
    "ounce*",
    "second*",
    "minute*",
    "hour*",
    "degree*",
    "celsius*",
    "fahrenheit*",
    "kelvin*",
    "meter* per second*",
    "kilometer* per hour*",
    "mile* per hour*",
    "liter*",
    "milliliter*",
    "cup*",
    "gallon*",
    "joule*",
    "calorie*",
    "kilowatt* hour*",
    "watt*",
    "kilowatt*",
    "degree*"]


for ru,en in zip(ru_word,en_word):
    translator.write_translation("ru",en,ru)
    translator.write_translation("en",en,en)

_ = translator.mark_translation()


#--------------------------------- Distance

class NLUnitKilometer(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("kilometer*"))
    key = unit.kilometer

class NLMeasurementKilometer(NLMeasurement):
    _unit_type = NLUnitKilometer


class NLUnitMeter(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("meter*"))
    key = unit.meter

class NLMeasurementMeter(NLMeasurement):
    _unit_type = NLUnitMeter


class NLUnitMile(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("mile*"))
    key = unit.mile

class NLMeasurementMile(NLMeasurement):
    _unit_type = NLUnitMile


class NLUnitFeet(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("foot*"))
    key = unit.feet

class NLMeasurementFeet(NLMeasurement):
    _unit_type = NLUnitFeet


class NLDistance(Group):
    _types = [
        NLMeasurementKilometer,
        NLMeasurementMeter,
        NLMeasurementFeet,
        NLMeasurementMile,
    ]

# ------------------------- Mass


class NLUnitGram(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("gram*"))
    key = unit.gram

class NLMeasurementGram(NLMeasurement):
    _unit_type = NLUnitGram


class NLUnitKilogram(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("kilogram*"))
    key = unit.kilogram

class NLMeasurementKilogram(NLMeasurement):
    _unit_type = NLUnitKilogram


class NLUnitPound(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("pound*"))
    key = unit.pound

class NLMeasurementPound(NLMeasurement):
    _unit_type = NLUnitPound


class NLUnitOunce(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("ounce*"))
    key = unit.ounce

class NLMeasurementOunce(NLMeasurement):
    _unit_type = NLUnitOunce


class NLMass(Group):
    _types = [
        NLMeasurementGram,
        NLMeasurementKilogram,
        NLMeasurementPound,
        NLMeasurementOunce,
    ]
    
# ----------------- Duration

class NLUnitSecond(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("second*"))
    key = unit.second

class NLMeasurementSecond(NLMeasurement):
    _unit_type = NLUnitSecond


class NLUnitMinute(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("minute*"))
    key = unit.minute

class NLMeasurementMinute(NLMeasurement):
    _unit_type = NLUnitMinute


class NLUnitHour(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("hour*")) 
    key = unit.hour

class NLMeasurementHour(NLMeasurement):
    _unit_type = NLUnitHour


class NLDuration(Group):
    _types = [
        NLMeasurementSecond,
        NLMeasurementMinute,
        NLMeasurementHour,
    ]

# ------------------- Temperature

class NLUnitCelsius(NLAbstractUnit):
    _unit_keywords = create_pattern(True, _("degree*")) + \
    create_pattern(False,_("celsius*")) 
    key = unit.celsius

class NLMeasurementCelsius(NLMeasurement):
    _unit_type = NLUnitCelsius


class NLUnitFahrenheit(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("fahrenheit*"))
    key = unit.fahrenheit

class NLMeasurementFahrenheit(NLMeasurement):
    _unit_type = NLUnitFahrenheit


class NLUnitKelvin(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("kelvin")) 
    key = unit.kelvin

class NLMeasurementKelvin(NLMeasurement):
    _unit_type = NLUnitKelvin


class NLTemperature(Group):
    _types = [
        NLMeasurementCelsius,
        NLMeasurementFahrenheit,
        NLMeasurementKelvin,
    ]

# -------------------------- Speed

class NLUnitMetersPerSecond(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("meter* per second*"))
    key = unit.meter / unit.second

class NLMeasurementMeterPerSecond(NLMeasurement):
    _unit_type = NLUnitMetersPerSecond


class NLUnitKilometersPerHour(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("kilometer* per hour*"))
    key = unit.kilometer / unit.hour

class NLMeasurementKilometersPerHour(NLMeasurement):
    _unit_type = NLUnitKilometersPerHour


class NLUnitMilesPerHour(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("mile* per hour*"))
    key = unit.mile / unit.hour

class NLMeasurementMilesPerHour(NLMeasurement):
    _unit_type = NLUnitMilesPerHour


class NLPeed(Group):
    _types = [
        NLMeasurementMeterPerSecond,
        NLMeasurementKilometersPerHour,
        NLMeasurementMilesPerHour,
    ]

# ------------------------- Volume

class NLUnitLiter(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("liter*"))
    key = unit.liter

class NLMeasurementLiter(NLMeasurement):
    _unit_type = NLUnitLiter


class NLUnitMililiter(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("milliliter*"))
    key = unit.milliliter

class NLMeasurementMililiter(NLMeasurement):
    _unit_type = NLUnitMililiter


class NLUnitCup(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("cup*"))
    key = unit.cup

class NLMeasurementCup(NLMeasurement):
    _unit_type = NLUnitCup


class NLUnitGallon(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("gallon*")) 
    key = unit.gallon

class NLMeasurementGallon(NLMeasurement):
    _unit_type = NLUnitGallon


class NLVolume(Group):
    _types = [
        NLMeasurementCup,
        NLMeasurementGallon,
        NLMeasurementMililiter,
        NLMeasurementLiter,
    ]

# ------------------------------------ Energy

class NLUnitJoul(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("joule*"))
    key = unit.joule

class NLMeasurementJoul(NLMeasurement):
    _unit_type = NLUnitJoul


class NLUnitCalories(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("calorie*"))
    key = unit.calorie 


class NLMeasurementCalories(NLMeasurement):
    _unit_type = NLUnitCalories


class NLUnitKilowattPerHour(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("kilowatt* hour*"))
    key = unit.kilowatt_hour

class NLMeasurementKilowattPerHour(NLMeasurement):
    _unit_type = NLUnitKilowattPerHour

class NLEnergy(Group):
    _types = [
        NLMeasurementKilowattPerHour,
        NLMeasurementCalories,
        NLMeasurementJoul,
    ]

# --------------------------- Power

class NLUnitWatt(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("watt*"))
    key = unit.watt

class NLMeasurementWatt(NLMeasurement):
    _unit_type = NLUnitWatt


class NLUnitKilowatt(NLAbstractUnit):
    _unit_keywords = create_pattern(False,_("kilowatt*"))
    key = unit.kilowatt

class NLMeasurementKilowatt(NLMeasurement):
    _unit_type = NLUnitKilowatt
    

class NLPower(Group):
    _types = [
        NLMeasurementKilowatt,
        NLMeasurementWatt,
    ]


def auto_register(module_globals):
    for obj in module_globals.values():
        if isinstance(obj,type) and issubclass(obj, (NLAbstractUnit, NLMeasurement, Group)):
            try:
                pattern_parser.register_parameter_type(obj)
            except Exception:
                pass

auto_register(globals())