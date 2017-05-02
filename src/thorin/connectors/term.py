"""A connector for the terminal. Useful for debugging."""


class Connector(object):
    """A connector for the terminal. Useful for debugging."""

    def __init__(self, parser):
        """Set the parser."""
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

    def send_message(self, room_id, msg):
        """Print Chattie's response."""
        print(msg)
