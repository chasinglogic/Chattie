"""A connector for the terminal. Useful for debugging."""


class Connector(object):
    """Connector class for the Telegram bot API."""

    def __init__(self, parser):
        """Will load the api token from $TELEGRAM_API_TOKEN."""
        self.parser = parser

    def listen(self):
        """Listen for messages."""
        print('Make sure to include your bot name in the message.'
              ' Type quit to exit.')

        while True:
            msg = input('>> ')
            if msg == 'quit':
                break
            self.parser(0, msg)

    def connect(self):
        """Simply here to match the expected interface."""
        pass

    def send_message(self, room_id, msg):
        """Print Thorin's response."""
        print(msg)
