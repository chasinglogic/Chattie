# Design Doc for Chattie 2.0

## Connector Design -- How we interface with external services

The connector design today looks like this:

```python
class Connector:
    """The base interface that must be implemented by a backend."""

    @abstractmethod
    def __init__(self, bot):
        """Bot is the parse_message function of the Bot class.

        It should be passed the room_id (whatever form that takes) and
        the plain text of the incoming message from the service.
        """
        self.bot = bot

    @abstractmethod
    def listen(self):
        """Should connect and listen to incoming messages from the backend.

        When an incoming message is parsed should send to self.parser
        (the Bot class' parse_message method)
        """
        raise NotImplementedError
```

Largely this API is staying the same however we are going to refactor the
internal code so that listen will run commands asynchronously / threaded.

Additionally the connector will now be responsible for both telling the bot to run command X and dealing with the return value.

## The Bot Class -- Changed in 2.0

Today the bot class looks like this:

```python
class Bot:
    """Base Bot class, maintains state and parsing commands."""

    def __init__(self, name, inventory, command_pkgs, handlers=[]):
        """Initialize the bot.

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
        self.inventory = inventory
        print("Inventory gathered...")

        self.handlers = handlers
        self.commands = {}
        for pkg in command_pkgs:
            loaded = pkg.load()
            self.commands.update(loaded.commands)

        # Add current directory PYTHONPATH for dynamic imports.
        sys.path.append(os.getcwd())

        # Check if tricks exists and add it if so.
        if exists('./tricks') or isfile('./tricks.py'):
            import tricks
            self.commands.update(tricks.commands)

        # Look for local handlers
        if exists('./handlers') or isfile('./handlers.py'):
            import handlers
            self.handlers += handlers.handlers

        print("Commands and handlers loaded...")

    def parse_message(self, msg, extras={}):
        """Parse the message, run any commands and handlers found. Returns an
        array of strings to send back to the channel."""
        print("Message received...")
        messages = []

        if self.name.lower() in msg.lower():
            print("Someone is talking to me...")
            split = msg.split(" ")

            # Start the cmd_idx at 1
            cmd_idx = 1

            # get the first word after our name as that will be the
            # command always.
            for i, w in enumerate(split):
                if w.lower().endswith(self.name.lower()):
                    cmd_idx = i + 1
                    break

            cmd = self.commands.get(split[cmd_idx])
            if cmd is None:
                return ["I don't know that trick."]

            resp = cmd(self, split, **extras)
            if resp:
                return [resp]

            return []

        # If no command then pass to handlers
        for h in self.handlers:
            reply = h(self, msg)
            if reply:
                messages.append(reply)

        return messages

    def get(self, key):
        """Alias to bot.inventory.get"""
        print("DEPRECATION WARNING: bot.get is deprecated, please use"
              " bot.inventory.get instead.")
        return self.inventory.get(key)

    def set(self, key, value):
        """Alias to bot.inventory.set"""
        print("DEPRECATION WARNING: bot.set is deprecated, please use"
              " bot.inventory.set instead.")
        return self.inventory.set(key, value)
```

There is a new API for the Bot class as well as a new class to describe an incoming Event from a connector. The connector will be responsible for turning an incoming message into an Event object.

```python
class Bot:

    def __init__(self, name, inventory, command_pkgs, handlers=[]):
        # Setup the bot
        pass
    
    def has_command(self, command):
        return True || False

    def run_command(self, command, **kwargs):
        return string_of_message_to_send

    def run_handlers(self, event, **kwargs):
        return [all_results_of_handlers_as_list_of_strings]
```

These are the major changes in 2.0 and will allow us to more easily extend
the model in the future as new needs come up.

Additionally for 2.0 I want to provide a Twitter connector as well as a Slack connector.