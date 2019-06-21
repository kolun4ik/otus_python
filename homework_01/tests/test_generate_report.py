import os
from datetime import datetime
import unittest
from unittest import skip
from .base import FunctionalTest
from log_analyzer import generate_report, config

DATA_SET = [
            {"count": 2767,
             "time_avg": 62.995,
             "time_max": 9843.569,
             "time_sum": 174306.352,
             "url": "/api/v2/internal/html5/phantomjs/queue/?wait=1m",
             "time_med": 60.073,
             "time_perc": 9.043,
             "count_perc": 0.106},
            {"count": 2567,
             "time_avg": 626.995,
             "time_max": 9843.569,
             "time_sum": 1754306.352,
             "url": "/api/v3/internal/html5/phantomjs/queue/?wait=1m",
             "time_med": 60.073,
             "time_perc":9.043,
             "count_perc": 0.106},
        ]

class GenerateReportTests(FunctionalTest):
    """Тестируем ф-цию генерации отчета"""

    # @skip('skip for testing')
    def test_generate_report_display_exception(self):
        """тест: возбуждает исключение, если директория ./reports не существует"""
        dir_fails = './reports_fail'
        with self.assertRaises(IOError):
            generate_report(dir_fails, DATA_SET)

    def test_template_exists_in_dir(self):
        """тест: шаблон отчета report.html находится в директории ./reports"""
        template = os.path.isfile(
            os.path.join(config['REPORT_DIR'], 'report.html'))
        self.assertTrue(template)

    def test_table_json_in_report_template(self):
        """тест: переменная $table_json существует в report.html"""
        with open(os.path.join(config['REPORT_DIR'], 'report.html'), 'r', encoding='utf-8') as file:
            template = file.read()
        self.assertIn('$table_json', template)

    def test_jquery_tablesorter_min_js_in_dir(self):
        """тест: jquery.tablesorter.min.js лежит в ./reports"""
        tablesorter = os.path.isfile(os.path.join(config['REPORT_DIR'], 'jquery.tablesorter.min.js'))
        self.assertTrue(tablesorter)

    def test_generate_report(self):
        """тест: генерируем отчет в директории ./reports, на выходе получаем файл
        вида report-YYYY.MM.DD.html, где YYYY.MM.DD - текущая дата отчета """
        now = datetime.strftime(datetime.now(), '%Y.%m.%d')
        report_name = f'report-{now}.html'
        generate_report(config['REPORT_DIR'], DATA_SET)
        reports = os.listdir(config['REPORT_DIR'])
        self.assertIn(
            report_name,
            reports
        )
        os.remove(os.path.join(config['REPORT_DIR'], report_name))


if __name__ == "__main__":
        unittest.main()