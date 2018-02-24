"""The primary Bot class which handles inventory and connections."""


class Bot:
    """Base Bot class, maintains state and parsing commands."""

    def __init__(self, name, inventory, commands={}, handlers=[]):
        """Initialize the bot.

        See the examples directory for commands, connectors, and handlers
        """
        print("Booting systems...")
        self.name = name
        print("Hello my name is " + name + "...")
        self.inventory = inventory
        print("Inventory gathered...")
        self.handlers = handlers
        self.commands = commands

    def run_command(self, command, msg, from_user='', mention_char='', **kwargs):
        fun = self.commands.get(command)
        if fun is None:
            return "Sorry, I don't know that trick.\n" + \
                self.commands['help'](self, msg, **kwargs)
        return fun(self, msg, **kwargs)

    def run_handlers(self, msg, from_user='', mention_char='', **kwargs):
        responses = []

        for handler in self.handlers:
            response = handler(self, msg, **kwargs)
            if response is not None:
                responses.append(response)

        return responses
