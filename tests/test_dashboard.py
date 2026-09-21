import unittest
from src.dashboard_data import build_data, correlation


class DashboardTests(unittest.TestCase):
    def test_correlation(self):
        self.assertAlmostEqual(correlation([(1, 3), (2, 6), (3, 9)]), 1)
        self.assertAlmostEqual(correlation([(1, 9), (2, 6), (3, 3)]), -1)
        self.assertIsNone(correlation([(1, 2)] * 3))
        self.assertIsNone(correlation([(1, 2)]))

    def test_local_data_integrity(self):
        data = build_data()
        keys = [(r['district'], r['year'], r['week']) for r in data['rows']]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertTrue(any(r['rainfall'] is not None for r in data['rows'] if r['district'] == 'Colombo'))
        self.assertTrue(all(r['rainfall'] is None for r in data['rows'] if r['district'] != 'Colombo'))
        self.assertEqual([r['lag'] for r in data['lags']], list(range(13)))
