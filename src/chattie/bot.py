"""The primary Bot class which handles inventory and connections."""

import json
import sys
import os

from os.path import isfile
from os.path import exists


class Bot:
    """Base Bot class, maintains state and parsing commands."""

    inventory = {}

    def __init__(self, name, connector, command_pkgs, handlers=[]):
        """Initialize the bot.

        connector should be a module which contains a class named
        Connector that follows the appropriate interface. See
        chattie.connectors for examples.

        command_pkgs should be a list of packages as returned by
        get_commands() from chattie.plugins. (essentially as returned
        by the entry_points functions)

        A command package needs to have a global dict variable named
        commands which contains a key for each command name and a
        corresponding value which is the function to call for that
        command. The command functions will be called with two
        arguments the first being the current instance of the Bot
        class the second will be an argv like array of the message.

        See the examples directory for commands, connectors, and handlers
        """
        print("Booting systems...")
        self.name = name
        print("Hello my name is " + name + "...")
        self.connector = connector.Connector(self.parse_message)
        if isfile("./inventory.json"):
            print("Loading my inventory from last time...")
            self.__load_inventory()
        self.handlers = handlers
        self.commands = {}
        for pkg in command_pkgs:
            loaded = pkg.load()
            self.commands.update(loaded.commands)

        # Add current directory PYTHONPATH for dynamic imports.
        sys.path.append(os.getcwd())

        # Check if tricks exists and add it if so.
        if exists('./tricks'):
            import tricks
            self.commands.update(tricks.commands)

        # Look for local handlers
        if exists('./handlers'):
            import handlers
            self.handlers += handlers.handlers

    def run(self):
        """Run the bot."""
        print("I am listening for messages...")
        self.connector.listen()

    def get(self, key):
        """Get key from the inventory."""
        return self.inventory[key]

    def set(self, key, value):
        """Save value in the inventory at key."""
        self.inventory[key] = value
        self.__save_inventory()

    def __load_inventory(self):
        """Load the inventory file from the filesystem.

        Potentially destructive function so we attempt to privatize it.
        """
        with open("./inventory.json", "r") as inv:
            self.inventory = json.load(inv)

    def __save_inventory(self):
        """Save the inventory to the file system.

        Potentially destructive function so we attempt to privatize it.
        """
        with open("./inventory.json", "w") as inv:
            json.dump(self.inventory, inv)

    def parse_message(self, room_id, msg):
        """Turn the message into an array and calls the requested command."""
        print("Message received...")
        if self.name.lower() in msg.lower():
            print("Someone is talking to me...")
            split = msg.split(" ")
            print("Parsed: ", split)
            # get the first word after our name as that will be the
            # command always.
            cmd_idx = 1
            for i, w in enumerate(split):
                if w.lower().endswith(self.name.lower()):
                    cmd_idx = i + 1
                    break

            cmd = self.commands.get(split[cmd_idx])
            if cmd is None:
                self.connector.send_message(room_id,
                                            'I don\'t know that trick.')
                return
            reply = cmd(self, split)
            self.connector.send_message(room_id, reply)
            return
        # If no command then pass to handlers
        for h in self.handlers:
            reply = h(self, msg)
            if reply:
                self.send_message(room_id, reply)
