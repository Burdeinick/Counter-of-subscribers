import unittest
import sys
sys.path.insert(0, 'Application')
from scripts.logic.add_new_group import AddGroup



class TestAddGroup(unittest.TestCase):
    """The class test some methods."""
    def setUp(self):
        self.addgroup = AddGroup().last_part_url

    def test_last_part_url(self):
        """Testing the 'last_part_url' method."""
        x = (('https://vk.com/animalplanetrussia', 'animalplanetrussia'), 
             ('zal_borcov', 'zal_borcov'),
             (12345, '12345'),
             ('', ''))

        for value in x:
            inp_d, extended = value[0], value[1]
            with self.subTest(x=value):
                self.assertEqual(self.addgroup(inp_d), extended)


if __name__ == "__main__":
    unittest.main()