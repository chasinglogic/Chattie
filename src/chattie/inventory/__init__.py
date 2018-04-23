
class Inventory:
    """Base Inventory class which all classes should inherit from."""

    def get(self, key, value):
        raise NotImplemented

    def set(self, key, value):
        raise NotImplemented
