from geopy.geocoders import Nominatim


def func(string:str):
    geolocator = Nominatim(user_agent="geo_app", timeout=1)
    location = geolocator.geocode(string)
    raw = location.raw
    loc_type = raw.get("type","")
    if loc_type in ("city", "administrative", "country", "residential"):
        print(f"DEBUG: {string} → type={loc_type}")
    else:
        print("Ем ну ем, на каком основании ты имешь ну ем указывать мною")


a = func("бердянск")
b = func("лондоне")
c = func("париже")
d = func("нью йорке")