"""The primary Bot class which handles inventory and connections."""

import json
import sys
import os

from os.path import isfile
from os.path import exists


class Bot:
    """Base Bot class, maintains state and parsing commands."""

    inventory = {}

    def __init__(self, name, inventory, command_pkgs, handlers=None):
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
        self.inventory = inventory
        print("Hello my name is " + name + "...")
        self.handlers = handlers if handlers else []
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

    def knows_command(self, command):
        return command in self.commands

    def run_command(self, command, msg, user=None):
        """Run command, return output of command."""
        cmd = self.commands.get(command)
        if cmd is None:
            return 'I don\'t know that trick.'
        return cmd(self, msg, user=None)

    def run_handlers(self, msg, user=None):
        """Run handlers, sends any output using send_message."""
        for h in self.handlers:
            reply = h(self, msg, user)
            if reply is None:
                continue
            yield reply
