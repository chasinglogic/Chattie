"""Contains methods for finding commands and connectors."""

import pkg_resources


def get_connectors():
    """Find all connectors available on the system."""
    return [v for v in
            pkg_resources.iter_entry_points('chattie.plugins.connectors')]


def get_commands():
    """Find all commands available on the system."""
    return [v for v in
            pkg_resources.iter_entry_points('chattie.plugins.tricks')]
