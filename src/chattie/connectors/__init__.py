"""The reference Connector class that defines the required interface."""


class Connector:
    """The base interface that must be implemented by a backend."""

    def __init__(self, parser):
        """Parser is the parse_message function of the Bot class.

        It should be passed the room_id (whatever form that takes) and
        the plain text of the incoming message from the service.
        """
        self.parser = parser

    def listen(self):
        """Should connect and listen to incoming messages from the backend.

        When an incoming message is parsed should send to self.parser
        (the Bot class' parse_message method)
        """
        pass

    def send_message(self, room_id, msg):
        """Send the msg to room_id.

        msg is always a plain string and room_id is whatever is passed
        to the Bot classes parse_message method as the room_id.
        """
        pass
