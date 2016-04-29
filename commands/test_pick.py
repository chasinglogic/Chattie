import unittest
import commands.pick as pick

class TestPick(unittest.TestCase):
    def test_choose(self):
        result = pick.choose("@thorin_bot pick jason justin mat")
        self.assertIn(result, ["jason", "justin", "mat"])

if __name__ == "__main__":
    unittest.main()
