"""A connector for the Telegram bot API.

This connector only requires the TELEGRAM_API_TOKEN environment
variable is set. You can acquire a token and instructions for making
your bot join rooms from here: https://core.telegram.org/bots
"""

import os

try:
    from telegram.ext import Updater
    from telegram.ext import MessageHandler
except ImportError:
    import sys
    print('You need to pip3 install python-telegram-bot before '
          'using this connector!')
    sys.exit(1)


class Connector:
    """Connector class for the Telegram bot API."""

    def __init__(self, bot):
        """Will load the api token from $TELEGRAM_API_TOKEN."""
        self.bot = bot

        token = os.getenv('TELEGRAM_API_TOKEN')
        if token is None:
            raise Exception('TELEGRAM_API_TOKEN not set')

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(MessageHandler(None, self.parse_incoming))

    def listen(self):
        """Listen for messages."""
        self.updater.start_polling()
        self.updater.idle()

    def parse_incoming(self, bot, incoming):
        """Transform incoming telegram info into format Chattie can parse."""
        resp = self.bot.parse_message(incoming.message.text)

        for r in resp:
            bot.sendMessage(chat_id=incoming.message.chat_id,
                            text=r)
