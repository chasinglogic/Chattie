import json
import chattie.inventory as inventory
from os.path import isfile


class Inventory(inventory.Inventory):
    """An inventory a class that has a get and set method serving
    as a key value store.

    This inventory is a simple JSON file dict-backed implementation and is
    simply a reference implementation for making more complex and useful
    inventories.
    """
    inventory = {}

    def __init__(self):
        """Init initializes the inventory."""
        if isfile("./inventory.json"):
            print("Loading my inventory from last time...")
            self.__load_inventory()

    def get(self, key):
        """Get the value for key."""
        return self.inventory.get(key, None)

    def set(self, key, value):
        """Set key to value."""
        self.inventory[key] = value
        self.__save_inventory()

    def __load_inventory(self):
        """Load the inventory file from the filesystem.

        Potentially destructive function so we attempt to privatize it.
        """
        with open("./inventory.json", "r") as inv:
            self.inventory = json.load(inv)

    def __save_inventory(self):
        """Save the inventory to the file system.

        Potentially destructive function so we attempt to privatize it.
        """
        with open("./inventory.json", "w") as inv:
            json.dump(self.inventory, inv)
