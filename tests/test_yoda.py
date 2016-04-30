import unittest
import commands.yoda as yoda

class TestYoda(unittest.TestCase):
    def test_translate(self):
        self.assertEqual("Lame, justin is", yoda.translate("Justin is lame"))
