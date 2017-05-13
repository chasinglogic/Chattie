"""A connector for the Telegram bot API.

This connector only requires the TELEGRAM_API_TOKEN environment
variable is set. You can acquire a token and instructions for making
your bot join rooms from here: https://core.telegram.org/bots
"""

import os

try:
    from telegram.ext import Updater
    from telegram.ext import MessageHandler
    from telegram.ext import CommandHandler
except ImportError:
    import sys
    print('You need to pip3 install python-telegram-bot before '
          'using this connector!')
    sys.exit(1)

from chattie.connectors import BaseConnector
from chattie.user import User


class Connector(BaseConnector):
    """Connector class for the Telegram bot API."""

    # Holds the bots for all given rooms
    bots = {}

    def __init__(self, bot):
        """Will load the api token from $TELEGRAM_API_TOKEN."""
        token = os.getenv('TELEGRAM_API_TOKEN')
        if token is None:
            raise Exception('TELEGRAM_API_TOKEN not set')
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.bot = bot

        self.dispatcher.add_handler(MessageHandler(None, self.parse_messages))
        for command, trick in self.bot.commands.items():
            self.dispatcher.add_handler(
                CommandHandler(
                    command,
                    self.parse_command(trick)
                )
            )

    def listen(self):
        """Listen for messages."""
        self.updater.start_polling()
        self.updater.idle()

    def send_message(self, room_id, msg):
        """Send a message to the given room_id."""
        self.bots[room_id].sendMessage(chat_id=room_id, text=msg)

    def get_username(self, update_user):
        """Return the username of a telegram user class."""
        return update_user.username

    def parse_command(self, trick):
        """Turns chattie commands into telegram CommandHandlers."""
        def tele_command(bot, update):
            response = trick(
                self.bot,
                update.message.text.split(' '),
                self.to_chattie_user(update.effective_user)
            )

            bot.sendMessage(
                chat_id=update.message.chat_id,
                text=response
            )

        return tele_command

    def parse_messages(self, bot, incoming):
        """Transform incoming telegram info into format Chattie can parse."""
        for reply in self.bot.dispatch_handlers(incoming.message.text):
            if reply:
                bot.sendMessage(chat_id=incoming.message.chat_id,
                                text=incoming.message.text)

    @staticmethod
    def to_chattie_user(tele_user):
        """Converts tele_user into Chattie user."""
        return User(
            full_name=tele_user.name,
            username=tele_user.username
        )
