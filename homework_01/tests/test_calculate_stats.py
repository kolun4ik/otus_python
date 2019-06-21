import unittest
from unittest import skip
from .base import FunctionalTest
from log_analyzer import calculate_statistics, config


TEST_DATA_IN = {"/api/v2/banner/25019354": [0.39, 0.246, 1.058, 1.955, 1.919, 1.398, 1.591, 0.246, 0.5, 2.265],}
EXCPECTED_DATA = [{
    "count": 10,
    "time_avg": 1.157,
    "time_max": 2.265,
    "time_sum": 11.568,
    "url": '/api/v2/banner/25019354',
    "time_med": 1.228,
    "time_perc": 100,
    "count_perc": 100}
]

class StatisticsCalculateTest(FunctionalTest):
    """Тестируем функцию расчетв статистики"""
    # @skip('skip test')
    def test_calculate_stats_return_list(self):
        """тест: калькулятор возвращает список словарей"""
        stat = calculate_statistics(TEST_DATA_IN, config['REPORT_SIZE'])
        self.assertEqual(stat[0]['count'], EXCPECTED_DATA[0]['count'])
        self.assertEqual(stat[0]['time_avg'], EXCPECTED_DATA[0]['time_avg'])
        self.assertEqual(stat[0]['time_max'], EXCPECTED_DATA[0]['time_max'])
        self.assertEqual(stat[0]['time_sum'], EXCPECTED_DATA[0]['time_sum'])
        self.assertEqual(stat[0]['url'], EXCPECTED_DATA[0]['url'])
        self.assertEqual(stat[0]['time_med'], EXCPECTED_DATA[0]['time_med'])
        self.assertEqual(stat[0]['time_perc'], EXCPECTED_DATA[0]['time_perc'])
        self.assertEqual(stat[0]['count_perc'], EXCPECTED_DATA[0]['count_perc'])


if __name__ == "__main__":
        unittest.main()