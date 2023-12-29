import unittest

import main1

class Test1(unittest.TestCase):

    def test(self):
        self.assertEqual(52, main1.hash('HASH'))