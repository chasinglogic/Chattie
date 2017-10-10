"""The default commands which come with Chattie."""

import requests
import random

from os import getenv
from inspect import getdoc


def helpcmd(bot, inc_msg):
    """Show the available commands and documentation."""
    try:
        msg = """
I know the following commands:

"""
        for name, fun in bot.commands.items():
            msg += """%s
--------
%s
========

""" % (name, getdoc(fun))
        return msg
    except:
        return 'Sorry, I don\'t know any commands'


def pick(bot, inc_msg):
    """Choose a random item from a list of things."""
    choices = inc_msg[inc_msg.index("pick") + 1:]
    return choices[random.randrange(0, len(choices))]


def the_rules(bot, incoming):
    """Print THE RULES."""
    return """The rules are:
    1. A robot may not injure a human being or, through
       inaction, allow a human being to come to harm.
    2. A robot must obey orders given it by human beings
       except where such orders would conflict with the First Law.
    3. A robot must protect its own existence as long as such
       protection does not conflict with the First or Second Law."""


def yoda(bot, inc_msg):
    """Attempt to translate the given message into yoda-speak."""
    msg = ' '.join(inc_msg[inc_msg.index('yoda') + 1:])
    url = "http://api.funtranslations.com/translate/yoda.json?text=" + msg
    r = requests.get(url)
    if r.status_code == 429:
        return "Sorry I can only translate 5 times per hour"
    try:
        return r.json()['contents']['translated'].replace("  ", " ")
    except:
        print(r.text)
        return "An unexpected error occured"


def hello(bot, incoming):
    """A simple ping style command for testing connectivity."""
    return "Wazzup"


JENKINS_URL = getenv("JENKINS_URL")
JENKINS_API_KEY = getenv("JENKINS_TOKEN")


def build(bot, inc_msg):
    """Run the given build in Jenkins."""
    r = requests.post(JENKINS_URL + "/job/" +
                      ' '.join(inc_msg[inc_msg.index("build") + 1:]) +
                      "/build?token=" + JENKINS_API_KEY)
    if r.status_code > 300:
        print("Error with the request:", r.text)
        return "I couldn't start the build."
    else:
        return "Build successfully started."


WEATHER_API_KEY = getenv("CHATTIE_WEATHER_API_TOKEN")


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
                     city + "&APPID=" + WEATHER_API_KEY + "&units=imperial")
    if r.status_code == 404:
        return "I can't find that city"
    if r.status_code > 300:
        return "Some unknown error occurred"
    return _format_resp(r.json())


# api.openweathermap.org/data/2.5/weather?zip={zip code}
def _get_weather_zip(zipcode):
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?zip="
                     + zipcode + "&APPID=" + WEATHER_API_KEY + "&units=imperial")
    if r.status_code == 404:
        return "I can't find that city"
    if r.status_code > 300:
        return "Some unknown error occurred"
    return _format_resp(r.json())


def weather(chattie, incoming):
    """Get the weather for a given city name or zip code."""
    city_or_zip = str(incoming[incoming.index("weather"):])
    if _is_zip_code(city_or_zip):
        return _get_weather_zip(city_or_zip)
    return _get_weather_name(city_or_zip)


commands = {
    'help': helpcmd,
    'pick': pick,
    'the_rules': the_rules,
    'yoda': yoda,
    'weather': weather,
    'hello': hello
}

if WEATHER_API_KEY:
    commands['weather'] = weather.weather

if JENKINS_API_KEY:
    commands['build'] = build
