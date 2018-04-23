"""A connector for the terminal. Useful for debugging.

It simply opens a REPL that lets you send "messages" to your bot.
"""


class Connector:
    """A connector for the terminal. Useful for debugging."""

    def __init__(self, bot):
        """Set the parser."""
        self.bot = bot

    def listen(self):
        """Listen for messages."""
        print('Commands start with ! use !help to see available commands.'
              ' All other messages will be passed to handlers.'
              ' Type quit to exit.')

        while True:
            msg = input('>> ')
            if msg == 'quit':
                break

            if msg.startswith('!'):
                command = msg.split(' ')[0]
                print(self.bot.run_command(command[1:], msg[1:]))
            else:
                for reply in self.bot.run_handlers(msg):
                    print(reply)
