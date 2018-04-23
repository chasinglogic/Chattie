import json
import os
from chattie.inventory import Inventory


class FileInventory(Inventory):
    """A simple file based JSON inventory system."""

    def __init__(self):
        self.inventory = {}
        self.ops = 0
        if os.path.isfile("./inventory.json"):
            print("Loading inventory from file...")
            self.__load_inventory()

    def get(self, key):
        """Get key from the inventory."""
        return self.inventory[key]

    def set(self, key, value):
        """Save value in the inventory at key."""
        self.inventory[key] = value
        self.ops += 1
        # Every 5 ops save the inventory to disk
        if self.ops >= 5:
            self.__save_inventory()
            self.ops = 0

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
