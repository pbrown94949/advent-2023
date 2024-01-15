import unittest

import main1


class Test1(unittest.TestCase):
    def test_conjunction_single_receives_high_impulse(self):
        conjunction = main1.Conjunction('a', ['b'], ['c'])
        message = main1.Message('b', 'a', main1.Pulse.HIGH)
        messages = conjunction.receive(message)
        self.assertEqual(main1.Pulse.LOW, messages[0].pulse)

    def test_conjunction_single_receives_low_impulse(self):
        conjunction = main1.Conjunction('a', ['b'], ['c'])
        message = main1.Message('b', 'a', main1.Pulse.LOW)
        messages = conjunction.receive(message)
        self.assertEqual(main1.Pulse.HIGH, messages[0].pulse)
