"""The reference Connector class that defines the required interface."""


class BaseConnector:
    """The base interface that must be implemented by a backend.

    You can inherit from this class to get nice error messages for the
    optional connector methods.
    """

    def __init__(self, bot):
        """Bot is a fully initiailzed bot instance.

        The connector is in charge of determining whether a command
        was asked for or whether handlers should be run instead.
        Once determined either the handlers can be run using the
        generator function bot.run_handlers or the method
        bot.run_command as appropriate. The return value will be a
        string to send back as a reply.
        """
        self.bot = bot

    def listen(self):
        """Should connect and listen to incoming messages from the backend."""
        raise NotImplemented
