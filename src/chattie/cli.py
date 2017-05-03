"""The cli for the chattie command."""

import click
import os

from chattie.bot import Bot
from chattie.tricks import helpcmd
from chattie.plugins import get_connectors
from chattie.plugins import get_commands


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
def commands():
    """Show all installed commands."""
    import chattie.connectors.term as term
    bot = Bot('Chattie', term, get_commands())
    print(helpcmd(bot, ''))


@chattie.command()
@click.argument('bot_name')
def new(bot_name):
    """Create a new bot directory."""
    os.mkdir(bot_name)
    os.mkdir(os.path.join(bot_name, 'tricks'))
    os.mkdir(os.path.join(bot_name, 'handlers'))

    with open(os.path.join(bot_name, 'envfile'), 'w') as f:
        f.write("""BOT_NAME=%s
# Use this if you want to use Telegram
# TELEGRAM_API_TOKEN='your token here'
""")

    with open(os.path.join(bot_name, 'README'), 'w') as f:
        f.write("""
How to use your new bot!

First you can write new commands or 'tricks' in tricks
""")


@chattie.command()
@click.option('--name',
              default=os.getenv('BOT_NAME', 'Chattie'),
              help='The name of your bot.')
@click.option('--connector',
              default=get_connectors()[0].name,
              help='Which connector to use, see "chattie connectors"')
def run(name, connector):
    """Run the bot.

    By default will run with the first available connector.
    """
    print('connect', connector)
    conn = None
    available = get_connectors()
    for c in available:
        if c.name == connector:
            print('Found connector')
            conn = c.load()

    if conn is None:
        conn = available[0].load()

    commands = get_commands()
    print('comm', commands)
    bot = Bot(name, conn, commands)
    bot.run()
