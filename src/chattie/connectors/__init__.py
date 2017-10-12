"""The reference Connector class that defines the required interface.

A Connector connects to any chat or backend service and handles delivering
incoming messages to the bot's parse_message method. It will then be
responsible for sending the responses from the bot back to the server."""

from abc import abstractmethod


class Connector:
    """The base interface that must be implemented by a backend."""

    @abstractmethod
    def __init__(self, bot):
        """Bot is the parse_message function of the Bot class.

        It should be passed the room_id (whatever form that takes) and
        the plain text of the incoming message from the service.
        """
        self.bot = bot

    @abstractmethod
    def listen(self):
        """Should connect and listen to incoming messages from the backend.

        When an incoming message is parsed should send to self.parser
        (the Bot class' parse_message method)
        """
        raise NotImplementedError
