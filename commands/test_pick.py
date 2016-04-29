import unittest
import pick

class PickTest(unittest.TestCase):
    def test_choose(self):
        result = choose("@thorin_bot pick jason justin mat")
        self.assertIn(result, ["jason", "justin", "mat"])

if __name__ == "__main__":
    unittest.main()
