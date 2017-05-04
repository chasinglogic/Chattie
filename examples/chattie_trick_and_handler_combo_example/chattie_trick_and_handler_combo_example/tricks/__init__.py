"""Example handlers for Chattie bot framework."""


def ping(bot, msg):
    """Respond with pong."""
    if 'pong' in msg:
        return 'pong.... wait a minute...'
    return 'pong'


commands = {
    'ping': ping,
    'pong': ping
}
