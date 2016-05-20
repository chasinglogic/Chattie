#!/usr/bin/python

import os
import sys
import json
import importlib

from os.path import isfile, join
from telegram.ext import Updater, MessageHandler

# Base bot class. Used for saving context etc.
class Bot:
    inventory = {}

    def __init__(self, name, token):
        print("Booting systems...")
        self.updater = Updater(token)
        print("Using API Token: " + token + "...")
        self.dispatch = self.updater.dispatcher
        print("Prepping dispatcher...")
        self.name = name.lower()
        print("Hello my name is " + name + "...")
        self.dispatch.addHandler(MessageHandler([], self.parse_message))
        if isfile("./inventory.json"):
            print("Loading my inventory from last time...")
            self.__load_inventory()

    def run(self):
        # self.start_scheduled_scripts()
        print("I am listening for messages...")
        self.updater.start_polling()
        self.updater.idle()

    # potentially destructive function so we attempt to privatize it
    def __load_inventory(self):
        with open("./inventory.json", "r") as inv:
            self.inventory = json.load(inv)

    def save_inventory(self):
        with open("./inventory.json", "w") as inv:
            json.dump(self.inventory, inv)

    def parse_message(self, bot, incoming):
        print("Message received...")
        if self.name in incoming.message.text.lower():
            print("Someone is talking to me...")
            split = incoming.message.text.lower().split(" ")
            print("Parsed: ", split)
            # get the first word after our name as that will be the command always.
            try:
                reply = self.run_command(split[split.index(self.name) + 1], incoming)
                print("Responding with " + reply + "...")
                bot.sendMessage(incoming.message.chat_id, text=reply)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                bot.sendMessage(incoming.message.chat_id, text="Sorry I had an errorerrorerrorerror")

    def run_command(self, command, incoming):
        reply = ""
        try:
            mod = importlib.import_module('commands.'+command)
            reply = mod.run(self, incoming)
        except:
            print("Unexpected error running command:", sys.exc_info()[1])
            if reply == "":
                return "Sorry I don't know that trick."
        return reply

# This is the bot to use for testing, it overrides methods with side effects to ease testing
# just use the run_command method for testing
class BotTest(Bot):
    def __init__(self, name):
        print("Booting systems...")
        print("Prepping dispatcher...")
        self.name = name.lower()
        print("Hello my name is " + name + "...")
        self.updater = Updater("")

    def make_mock_message(msg):
        message = Message(0, None, None, None, text=msg)
        return message

        

if __name__ == "__main__":
    bot = Bot("@Thorin_Bot", os.getenv("THORIN_API_TOKEN"))
    bot.run()
