"""The cli for the thorin command."""

import click

from thorin.bot import Bot
from thorin.plugins import get_connectors
from thorin.plugins import get_commands


@click.group()
def thorin():
    """Helpful commands for running a thorin bot."""
    pass


@thorin.command()
def connectors():
    """Show all installed connectors."""
    connectors = get_connectors()
    for c in connectors:
        print(c.name)


@thorin.command()
def commands():
    """Show all installed commands."""
    commands = get_commands()
    for c in commands:
        print(c.name)


@thorin.command()
@click.option('--name',
              default='Thorin',
              help='The name of your bot.')
@click.option('--connector',
              default=get_connectors()[0].name,
              help='Which connector to use, see "thorin connectors"')
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
