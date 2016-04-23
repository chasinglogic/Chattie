import os
import importlib

from os.path import isfile, join
from telegram.ext import Updater
from threading import Timer

# Base bot class. Used for saving context etc.
class Bot:
    hourly_tasks = []
    daily_tasks = []
    greetings = ["hey", "hello", "hi"]
    inventory = {}

    def __init__(self, name, token):
        self.updater = Updater(token)
        self.dispatch = updater.dispatcher
        self.name = name
        self.dispatch.addTelegramMessageHandler(self.parse_message)

    def run(self):
        self.start_scheduled_scripts()
        self.updater.start_polling()
        self.updater.idle()

    def parse_message(self, bot, incoming):
        if self.name in message:
            split = incoming.message.text.split(" ")
            # get the first word after our name as that will be the command always.
            reply = self.run_command(split[split.index(self.name) + 1], incoming)
            bot.sendMessage(incoming.message.chat_id, text=reply)

    def run_command(self, command, incoming):
        reply = ""

        if any(greeting in incoming.message.text.lower() for greeting in self.greetings):
            reply += "What's up bro?\n"

        if "the rules" in incoming.message.text.lower():
            reply += """The rules are: 
    1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.
    2. A robot must obey orders given it by human beings except where such orders would conflict with the First Law.
    3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law."""

        try:
            command = importlib.import_module('commands.'+command)
            reply += command.run(self, incoming)
        except:
            if reply == "":
                return "Sorry I don't know that trick."

        return reply

    def run_hourly():
        self.hourly_tasks = [ f for f in os.listdir("./scheduled/hourly") if "init" not in f ]
        for task in hourly_tasks:
            fun = importlib.import_module("scheduled.hourly."+task.strip(".py"))
            notification = fun.run()
            self.updater.send_message(notification)
        Timer(3600, self.run_hourly).start()

    def run_daily():
        self.daily_tasks = [ f for f in os.listdir("./scheduled/daily") if "init" not in f ]
        for task in daily_tasks:
            fun = importlib.import_module("scheduled.daily."+task.strip(".py"))
            notification = fun.run()
            self.updater.send_message(notification)
        Timer(86400, self.run_daily).start()
        return ""

    def start_scheduled_scripts(self):
        self.run_hourly()
        self.run_daily()


