"""The cli for the chattie command."""

import click
import os
import sys

from inspect import getdoc
from chattie.bot import Bot
from chattie.tricks import helpcmd
from chattie.plugins import get_connectors
from chattie.plugins import get_commands
from chattie.plugins import get_inventories


def load_commands():
    """Load the commands for our bot.

    A command package needs to have a global dict variable named
    commands which contains a key for each command name and a
    corresponding value which is the function to call for that
    command. The command functions will be called with two
    arguments the first being the current instance of the Bot
    class the second will be an argv like array of the message.
    """
    commands = {}
    for pkg in get_commands():
        loaded = pkg.load()
        commands.update(loaded.commands)

    # Check if tricks exists and add it if so.
    try:
        import tricks
        commands.update(tricks.commands)
    except ImportError:
        pass

    return commands


@click.group()
def chattie():
    """Helpful commands for running a chattie bot."""
    pass


@chattie.command()
def connectors():
    """Show all installed connectors."""
    connectors = get_connectors()
    for c in connectors:
        print(c.name)


@chattie.command()
def inventories():
    """Show all installed inventories."""
    inventories = get_inventories()
    for i in inventories:
        print(i.name)


@chattie.command()
@click.argument('connector_name')
def doc(connector_name):
    """View the doc for the given connector."""
    connectors = get_connectors()
    for c in connectors:
        if c.name == connector_name:
            print(getdoc(c.load()))


@chattie.command()
@click.argument('inventory_name')
def idoc(inventory_name):
    """View the doc for the given inventory."""
    inventories = get_inventories()
    for c in inventories:
        if c.name == inventory_name:
            print(getdoc(c.load()))


@chattie.command()
def commands():
    """Show all installed commands."""
    import chattie.connectors.term as term
    bot = Bot('Chattie', term, load_commands())
    print(helpcmd(bot, ''))


@chattie.command()
@click.argument('bot_name')
def new(bot_name):
    """Create a new bot."""
    os.mkdir(bot_name)
    # Create the tricks directory
    os.mkdir(os.path.join(bot_name, 'tricks'))
    with open(os.path.join(bot_name, 'tricks', '__init__.py'), 'w') as f:
        f.write("commands = {}")
    # Create the handlers directory
    os.mkdir(os.path.join(bot_name, 'handlers'))
    with open(os.path.join(bot_name, 'handlers', '__init__.py'), 'w') as f:
        f.write("handlers = []")

    with open(os.path.join(bot_name, 'envfile'), 'w') as f:
        f.write("""export BOT_NAME={bot_name}

######################################################################
#                   Telegram Connector Config                        #
######################################################################
# Make sure you install python-telegram-bot first with
# pip3 install python-telegram-bot
# export TELEGRAM_API_TOKEN='your token here'

######################################################################
#                   Matrix Connector Config                          #
######################################################################
# Make sure you install matrix_client first with
# pip3 install matrix_client
# export MATRIX_URL='https://matrix.org'
# export MATRIX_USERNAME={bot_name}
# export MATRIX_PASSWORD='my_bots_password'
# Comma seperated list of rooms to join
# export MATRIX_ROOMS='#thorin-test:matrix.org'""".format(bot_name=bot_name))

    with open(os.path.join(bot_name, 'README'), 'w') as f:
        f.write("""How to use your new bot!

First you can write new commands or 'tricks' in the tricks folder and
new handlers in the handlers folder. If that doesn't make sense to you
you can view the documentation at:

https://github.com/chasinglogic/Chattie

Now if you want to just run your bot you need to first pick a
connector. To view installed connectors run:

chattie connectors

Once you've picked a connector then set the appropriate environment
variables in envfile then activate it with:

source envfile

Finally:

chattie run --connector connector_name

and you're good to go!
""")


@chattie.command()
@click.option('--name',
              default=os.getenv('BOT_NAME', 'chattie'),
              help='The name of your bot.')
@click.option('--connector',
              default='terminal',
              help='Which connector to use, see "chattie connectors"')
@click.option('--inventory',
              default='json',
              help='Which inventory to use, see "chattie inventories"')
def run(name, connector, inventory):
    """Run the bot.

    By default will run with the first available connector.
    """
    connectors = get_connectors()
    if len(connectors) == 0:
        print("ERROR: No available connectors!")
        sys.exit(1)

    conn_pkg = None
    for c in connectors:
        if c.name == connector:
            conn_pkg = c.load()

    if conn_pkg is None:
        print("ERROR: No valid connector given.")
        sys.exit(1)

    inventories = get_inventories()
    if len(inventories) == 0:
        print("ERROR: No available inventories!")
        sys.exit(1)

    for i in inventories:
        if i.name == inventory:
            inventory_pkg = i.load()

    # Add current directory PYTHONPATH for dynamic imports.
    sys.path.append(os.getcwd())

    # Load commands from entry_points and local tricks
    commands = load_commands()

    handlers = []
    # Look for local handlers
    try:
        import handlers
        handlers += handlers.handlers
    except ImportError:
        pass

    inventory = inventory_pkg.Inventory()
    bot = Bot(name, inventory, commands, handlers)
    connector = conn_pkg.Connector(bot)
    print("Listening for messages...")
    connector.listen()


if __name__ == '__main__':
    chattie()
