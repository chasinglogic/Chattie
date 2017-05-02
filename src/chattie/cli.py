"""The cli for the chattie command."""

import click

from chattie.bot import Bot
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
    commands = get_commands()
    for c in commands:
        print(c.name)


@chattie.command()
@click.option('--name',
              default='Chattie',
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
