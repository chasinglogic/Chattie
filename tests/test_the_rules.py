import unittest
import commands.the_rules as rules

class TestTheRules(unittest.TestCase):
    def test_the_rules(self):
       self.assertEqual("""The rules are: 
    1. A robot may not injure a human being or, through inaction, allow a human being to come to harm.
    2. A robot must obey orders given it by human beings except where such orders would conflict with the First Law.
    3. A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.""",
       rules.run(None, None))
