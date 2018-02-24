"""A connector for the terminal. Useful for debugging.

It simply opens a REPL that lets you send "messages" to your bot.
"""


class Connector:
    """A connector for the terminal. Useful for debugging."""

    def __init__(self, bot):
        """Set the bot."""
        self.bot = bot

    def parse_command(self, msg):
        if not msg.startswith('!'):
            return None
        command = ''
        for char in msg[1:]:
            if char == ' ':
                break
            command += char
        return command

    def listen(self):
        """Listen for messages."""
        print('Type messages to your bot. Commands start with ! (ex. !help).'
              ' Handlers will be run if the message is not a command.'
              ' Type quit to exit.')

        while True:
            msg = input('>> ')
            if msg == 'quit':
                break

            command = self.parse_command(msg)
            if command is not None:
                response = self.bot.run_command(command, msg)
                print(response)
            else:
                responses = self.bot.run_handlers(msg)
                for response in responses:
                    print(response)
