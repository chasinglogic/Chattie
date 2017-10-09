"""Contains methods for finding commands and connectors."""

import pkg_resources


def get_inventories():
    """Find all inventories available on the system."""
    return [v for v in
            pkg_resources.iter_entry_points('chattie.plugins.inventories')]


def get_connectors():
    """Find all connectors available on the system."""
    return [v for v in
            pkg_resources.iter_entry_points('chattie.plugins.connectors')]


def get_commands():
    """Find all commands available on the system."""
    return [v for v in
            pkg_resources.iter_entry_points('chattie.plugins.tricks')]


def get_handlers():
    """Find all handlers available on the system."""
    mods = [v.load() for v in
            pkg_resources.iter_entry_points('chattie.plugins.handlers')]
    handlers = []
    for m in mods:
        handlers += m.handlers
    return handlers
