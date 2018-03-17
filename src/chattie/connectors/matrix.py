"""A Chattie connector for Matrix.

This connector requires that you register an account for the bot
before setting up a connection

Requires the following environment variables:

MATRIX_URL -- The Matrix homeserver, such as https://matrix.org
MATRIX_USERNAME -- The bot username
MATRIX_PASSWORD -- The bot password
MATRIX_ROOMS -- a comma seperated list of rooms for the bot to join
"""

import os
import chattie.connectors as connectors

try:
    from matrix_client.client import MatrixRequestError
    from matrix_client.client import MatrixClient
except ImportError:
    import sys
    print('You need to pip3 install matrix_client before '
          'using this connector!')
    sys.exit(1)

MATRIX_URL = os.getenv("MATRIX_URL")
MATRIX_USERNAME = os.getenv("MATRIX_USERNAME")
MATRIX_PASSWORD = os.getenv("MATRIX_PASSWORD")
MATRIX_ROOMS = os.getenv("MATRIX_ROOMS")

if None in [MATRIX_URL, MATRIX_USERNAME, MATRIX_PASSWORD, MATRIX_ROOMS]:
    print('You must set MATRIX_URL, MATRIX_USERNAME, MATRIX_PASSWORD, and '
          'MATRIX_ROOMS environment variables to use this connector.')
    print('Missing variables:',
          [missing[0] for missing in
           [
               ('MATRIX_URL', MATRIX_URL),
               ('MATRIX_USERNAME', MATRIX_USERNAME),
               ('MATRIX_PASSWORD', MATRIX_PASSWORD),
               ('MATRIX_ROOMS', MATRIX_ROOMS)
           ]
           if missing[1] is None])
    import sys
    sys.exit(1)


class Connector(connectors.Connector):
    """A matrix connector for the Chattie bot framework."""

    def __init__(self, bot):
        """Connect to the matrix room."""
        self.bot = bot

        self.client = MatrixClient(MATRIX_URL)
        # Try to register if it fails try to log in.
        try:
            self.token = self.client.\
                         register_with_password(username=MATRIX_USERNAME,
                                                password=MATRIX_PASSWORD)
        except MatrixRequestError:
            self.token = self.client.\
                         login_with_password(username=MATRIX_USERNAME,
                                             password=MATRIX_PASSWORD)
        for room in MATRIX_ROOMS.split(","):
            room_name = room
            if not room.startswith("#"):
                room_name = "!" + room
            r = self.client.join_room(room_name)
            r.add_listener(self.parse_event)

    def listen(self):
        """Listen for messages on Matrix."""
        self.client.listen_forever()

    def parse_event(self, room, event):
        """Transform Matrix incoming_event to text."""
        if event['type'] != 'm.room.message':
            return

        resp = self.bot.parse_message(event['content']['body'])

        for r in resp:
            room.send_text(r)
