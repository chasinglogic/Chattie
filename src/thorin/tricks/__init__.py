"""The default commands which come with Thorin."""

import requests
import random
import thorin.tricks.weather as weather

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


commands = {
    'help': helpcmd,
    'pick': pick,
    'the_rules': the_rules,
    'yoda': yoda,
    'hello': hello
}

# if weather.API_KEY:
#     commands['weather'] = weather.weather

if JENKINS_API_KEY:
    commands['build'] = build
