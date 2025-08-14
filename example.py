# with open('cities.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)


# c = "Nikolaev"


# country_code:set[str] = set()

# def find_city(city:str):
#     for i in data:
#         print(i["name"], i["latitude"], i["longitude"], i["country_code"])
#         country_code.add(i["country_code"])
#         if i["name"] == city:
#             #print()
#             return i["name"]
#             #yield city

# func = find_city(c)

# for code in country_code:
#     try:
#         translate = Translator(code.capitalize())

#         if "IS AN INVALID TARGET LANGUAGE" not in translate.translate(func):
#             print(f"{code}",translate.translate(func))
#         else:
#             pass
#     except RuntimeError : ...

# print(country_code)
# for i in func:
#     print(i)
