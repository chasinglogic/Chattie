"""The primary Bot class which handles inventory and connections."""

import json

from os.path import isfile


class Bot(object):
    """Base Bot class, maintains state and parsing commands."""

    inventory = {}

    def __init__(self, name, connector, command_pkgs):
        """Initialize the bot.

        connector should be a module which contains a class named
        Connector that follows the appropriate interface. See
        thorin.connectors for examples.

        command_pkgs should be a list of packages as returned by
        get_commands() from thorin.plugins. (essentially as returned
        by the entry_points functions)

        A command package needs to have a global dict variable named
        commands which contains a key for each command name and a
        corresponding value which is the function to call for that
        command. The command functions will be called with two
        arguments the first being the current instance of the Bot
        class the second will be an argv like array of the message.
        """
        print("Booting systems...")
        self.name = name
        print("Hello my name is " + name + "...")
        self.connector = connector.Connector(self.parse_message)
        if isfile("./inventory.json"):
            print("Loading my inventory from last time...")
            self.__load_inventory()
        self.commands = {}
        for pkg in command_pkgs:
            loaded = pkg.load()
            self.commands.update(loaded.commands)

    def run(self):
        """Run the bot."""
        print("I am listening for messages...")
        self.connector.listen()

    def __load_inventory(self):
        """Load the inventory file from the filesystem.

        Potentially destructive function so we attempt to privatize it.
        """
        with open("./inventory.json", "r") as inv:
            self.inventory = json.load(inv)

    def save_inventory(self):
        """Save the inventory to the file system."""
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
            try:
                cmd_idx = split.index(self.name) + 1
            except ValueError:
                cmd_idx = split.index(self.name.lower()) + 1
            cmd = self.commands.get(split[cmd_idx])
            if cmd is None:
                self.connector.send_message(room_id,
                                            'I don\'t know that trick.')
                return
            reply = cmd(self, split)
            self.connector.send_message(room_id, reply)
