import unittest
from datetime import datetime
from gedcom_parse import birth_before_death


class TestUserStory3(unittest.TestCase):
    def test_birth_before_death(self):
        # Test case where birth date is before death date
        self.assertTrue(birth_before_death("@I1@"))
        self.assertTrue(birth_before_death("@I2@"))

        # # Test case where birth date is after death date
        # self.assertFalse(birth_before_death("@I100@"))

        # # Test case where birth date is the same as death date
        # self.assertFalse(birth_before_death("@I101@"))


if __name__ == '__main__':
    unittest.main()
