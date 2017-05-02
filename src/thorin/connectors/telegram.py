"""A connector for the Telegram bot API."""

import os

from telegram.ext import Updater
from telegram.ext import MessageHandler


class Connector(object):
    """Connector class for the Telegram bot API."""

    # Holds the bots for all given rooms
    bots = {}

    def __init__(self, parser):
        """Will load the api token from $TELEGRAM_API_TOKEN."""
        token = os.getenv('TELEGRAM_API_TOKEN')
        if token is None:
            raise Exception('TELEGRAM_API_TOKEN not set')
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher
        self.parser = parser
        self.dispatch.addHandler(MessageHandler([], self.parse_incoming))

    def listen(self):
        """Listen for messages."""
        self.updater.start_polling()
        self.updater.idle()

    def connect(self):
        """Connect to the rooms specified by TELEGRAM_ROOMS.

        TELEGRAM_ROOMS can be a comma seperated list of room names.
        """
        rooms = os.getenv('TELEGRAM_ROOMS')
        if rooms is None:
            raise Exception('TELEGRAM_ROOMS not set')

    def send_message(self, room_id, msg):
        """Send a message to the given room_id."""
        self.bots[room_id].sendMessage(room_id, text=msg)

    def parse_incoming(self, bot, incoming):
        """Transform incoming telegram info into format Thorin can parse."""
        self.parser(incoming.message.chat_id, incoming.message.text)
        self.bots[incoming.message.chat_id] = bot
