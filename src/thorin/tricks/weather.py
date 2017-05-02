"""A simple weather command for Thorin."""

import requests
from os import getenv

API_KEY = getenv("THORIN_WEATHER_API_TOKEN")


def _is_zip_code(requested):
    try:
        int(requested)
        return True
    except:
        return False


def _format_resp(jsn):
    return 'Temperature: %s Condition: %s'.format(
        jsn['main']['temp'],
        jsn['weather'][0]['description']
    )


# We make a call to:
# api.openweathermap.org/data/2.5/weather?q={city name}
def _get_weather_name(city):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" +
                     city + "&APPID=" + API_KEY + "&units=imperial")
    if r.status_code == 404:
        return "I can't find that city"
    if r.status_code > 300:
        return "Some unknown error occurred"
    return _format_resp(r.json())


# api.openweathermap.org/data/2.5/weather?zip={zip code}
def _get_weather_zip(zipcode):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?zip="
                     + zipcode + "&APPID=" + API_KEY + "&units=imperial")
    if r.status_code == 404:
        return "I can't find that city"
    if r.status_code > 300:
        return "Some unknown error occurred"
    return _format_resp(r.json())


def weather(thorin, incoming):
    """Get the weather for a given city name or zip code."""
    city_or_zip = str(incoming[incoming.index("weather"):])
    if _is_zip_code(city_or_zip):
        return _get_weather_zip(city_or_zip)
    return _get_weather_name(city_or_zip)
