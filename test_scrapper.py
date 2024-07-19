import unittest
import scrapper

class TestScrapper(unittest.TestCase):

    def test_titles(self):
        titles = scrapper()[0]
        self.assertEqual(titles, ('Engine', 'Origin', 'Designer', 'Vehicle', 'Status', 'Use', 'Propellant', 'Power cycle', 'Specific impulse Vac (s)', 'Specific impulse SL (s)', 'Thrust Vac (N)', 'Thrust SL (N)', 'Chamber pressure (bar)', 'Mass (kg)', 'Thrust:weight ratio', 'Oxidiser:fuel ratio'))
    def test_data(self):
        data = scrapper()[1]
        for i in range(len(data) - 1):
            self.assertEqual(len(data[i]), 16)

if __name__ == '__main__':
    unittest.main()
