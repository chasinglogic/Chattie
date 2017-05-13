"""Contains definition of the Chattie user class"""


class User:
    """A common user interface to normalize user objects across connectors."""
    def __init__(self, *, username="", full_name="", email=""):
        self.username = username
        self.full_name = full_name
        self.email = email
