import unittest
import commands.yoda as yoda

class TestYoda(unittest.TestCase):
    def test_translate(self):
        self.assertIn(yoda.translate("Justin is lame"), 
                ["Lame, justin is", "Sorry I can only translate 5 times per hour"])
