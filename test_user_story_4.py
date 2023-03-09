import unittest
from datetime import datetime
from gedcom_parse import marriage_before_divorce


class TestUserStory3(unittest.TestCase):
    def test_birth_before_death(self):
        # Test case where marriage is before divorce
        self.assertTrue(marriage_before_divorce("@I1@"))
        self.assertTrue(marriage_before_divorce("@I2@"))


if __name__ == '__main__':
    unittest.main()
