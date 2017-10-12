import unittest
from chattie.bot import Bot
from chattie.plugins import get_commands
from chattie.inventory.json import Inventory


class TestTricks(unittest.TestCase):

    def setUp(self):
        self.bot = Bot("test", Inventory(), get_commands())

    def test_yoda(self):
        self.assertIn(self.bot.parse_message("test yoda Justin is lame")[0],
                      ["Lame, justin is",
                       "Sorry I can only translate 5 times per hour"])

    def test_pick(self):
        result = self.bot.parse_message("test pick jason justin mat")
        self.assertIn(result[0], ["jason", "justin", "mat"])

    def test_hello(self):
        result = self.bot.parse_message("test hello")
        self.assertEqual(result[0], "Wazzup")

    def test_the_rules(self):
        result = self.bot.parse_message("test the_rules")
        self.assertEqual("""The rules are:
    1. A robot may not injure a human being or, through
       inaction, allow a human being to come to harm.
    2. A robot must obey orders given it by human beings
       except where such orders would conflict with the First Law.
    3. A robot must protect its own existence as long as such
       protection does not conflict with the First or Second Law.""",
                         result[0])
