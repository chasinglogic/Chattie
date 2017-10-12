"""A connector for the terminal. Useful for debugging.

It simply opens a REPL that lets you send "messages" to your bot.
"""


class Connector:
    """A connector for the terminal. Useful for debugging."""

    def __init__(self, bot):
        """Set the bot."""
        self.bot = bot

    def listen(self):
        """Listen for messages."""
        print('Make sure to include your bot name in the message.'
              ' Type quit to exit.')

        while True:
            msg = input('>> ')
            if msg == 'quit':
                break

            resp = self.bot.parse_message(msg)
            for r in resp:
                print(r)
