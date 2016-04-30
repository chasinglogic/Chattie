import unittest
import commands.hello as hello

class TestHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual("Wazzup", hello.run(None, None))
