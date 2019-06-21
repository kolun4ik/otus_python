import os
import gzip
import shutil
import unittest
from datetime import datetime
from random import random, randint
from .base import FunctionalTest
from collections import defaultdict
from log_analyzer import parser_log_statistics, regexp, config
from unittest import skip


class ParserLogStatTests(FunctionalTest):
    """Тестируем ф-цию распарсивания лога nginx и сбора
     статистики для последующего анализа"""

    def create_test_logs(self, num_line, threshold=False):
        """имитируем лог Nginx"""
        now = datetime.strftime(datetime.now(), '%Y%m%d')
        log_name = 'nginx-access-ui.log-%s' % now
        with open(os.path.join(config['LOG_DIR'],log_name),'w') as log:
            for _ in range(num_line):
                line = '1.196.116.32 -  - [] "GET /api/%s HTTP/1.1" 200 927 "-" "-" "-" "-" "-" %s\n' % (
                    randint(1,5),
                    round(random(), 3) if threshold is False else '-')
                log.write(line)
        return log_name

    def test_regexp_for_parsing(self):
        """тест: регулярное выражение правильно парсит несколько строк лога"""
        logs = b'''1.196.116.32 -  - [] "GET /api/v2 HTTP/1.1" 200 927 "-" "-" "-" "-" "-" 0.390'''
        self.assertRegex(logs, regexp)

    def test_open_log_file_as_plain_text(self):
        """тест: парсер может обработать лог, как файл plain text"""
        log = self.create_test_logs(num_line=10)
        data = parser_log_statistics(config['LOG_DIR'], log)
        self.assertIsInstance(data, defaultdict)

    # @skip('skip this test')
    def test_open_log_file_as_gzip(self):
        """проверяем, что парсер может обработать лог, как архив gzip"""
        log = self.create_test_logs(10)
        log_gz = log + '.gz'
        with open(os.path.join(config['LOG_DIR'],log), 'rb') as f_in:
            with gzip.open(os.path.join(config['LOG_DIR'],log_gz), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        data = parser_log_statistics(config['LOG_DIR'], log_gz)
        # Пока не знаю какую проверку применить для этого случая
        self.assertIsInstance(data, defaultdict)

    def test_threshold_generate_exception(self):
        """тест: при превышении порога ошибок парсинга возбуждаем исключение"""
        log = self.create_test_logs(10, threshold=True)
        with self.assertRaises(OverflowError):
            parser_log_statistics(config['LOG_DIR'], log)


if __name__ == "__main__":
        unittest.main()