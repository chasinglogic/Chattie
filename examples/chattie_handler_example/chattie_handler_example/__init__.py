"""Example handlers for Chattie bot framework."""


def counter(bot, msg):
    """Count the number of times count is said.

    Returns nothing so no message is sent back to the chat.
    """
    if 'count' in msg.lower():
        count = bot.get('count_count')
        count += 1
        bot.set('count_count', count)


def stealth_mountain(bot, msg):
    """Imitate the @StealthMountain twitter bot."""
    if 'sneak peak' in msg.lower():
        return 'Did you mean sneak peek?'


handlers = [
    counter,
    stealth_mountain
]
