import requests
from os import getenv

API_KEY = getenv("THORIN_WEATHER_API_TOKEN")

def is_zip_code(requested):
    try:
        int(requested)
        return True
    except:
        return False

# We make a call to:
# api.openweathermap.org/data/2.5/weather?q={city name}
def get_weather_name(city):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&APPID=" + API_KEY + "&units=imperial")
    if r.status_code == 404:
        return "I can't find that city"
    if r.status_code > 300:
        return "Some unknown error occurred"
    return str(r.json()['main']['temp']) + " " + r.json()['weather'][0]['description']

# api.openweathermap.org/data/2.5/weather?zip={zip code}
def get_weather_zip(zipcode):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "&APPID=" + API_KEY + "&units=imperial")
    if r.status_code == 404:
        return "I can't find that city"
    if r.status_code > 300:
        return "Some unknown error occurred"
    return str(r.json()['main']['temp']) + " " + r.json()['weather'][0]['description']

def run(thorin, incoming):
    split = incoming.message.text.split(" ")
    city_or_zip = str(split[split.index("weather"):])
    if is_zip_code(city_or_zip):
        return get_weather_zip(city_or_zip)
    return get_weather_name(city_or_zip)
