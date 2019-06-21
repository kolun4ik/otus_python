import os
import gzip
import unittest
from .base import FunctionalTest
from datetime import datetime
from log_analyzer import latest_log_get, config


class LatestLogGetTests(FunctionalTest):
    """тест: тестируем ф-цию получения самого свежего
     лога NGINX в дирекории с логами"""

    def test_generate_warning_if_log_dir_not_exist(self):
        """тест: ожидаем исключение, если директория с логами
         не существует и выходим, не является ошибкой"""
        dir_fails = './log_fail'
        with self.assertRaises(IOError):
            latest_log_get(dir_fails)

    def test_generate_raise_if_nginx_log_not_exist(self):
        """тест: ожидаем исключение, если в log_dir
        отсутствуют логи nginx"""
        with self.assertRaises(IOError):
            latest_log_get(config['LOG_DIR'])

    def test_search_last_log_nginx_in_log_dir(self):
        """тест: поиск самаго свежего файла лога nginx в директории с логами"""
        now = 'nginx-access-ui.log-%s' % datetime.strftime(datetime.now(), '%Y%m%d')
        log_files = [now]
        for i in range(5):
            nginx_log = 'nginx-access-ui.log-%s' % self.random_date_gen(
                start='01.01.2017',
                end='04.05.2019')
            other_log = 'apache_accees-ui.log-%s' % self.random_date_gen(
                start='01.01.2017',
                end='19.05.2019')
            log_files.append(nginx_log)
            log_files.append(other_log)
        for file in log_files:
            with open(os.path.join(config['LOG_DIR'], file), 'w'):
                pass
        last_log = latest_log_get(config['LOG_DIR'])
        self.assertEqual(last_log.name, now)

    def test_return_named_tuple(self):
        """тест: что в именованый кортеж возвращается с полями:
         path, name, creation_date, extention"""
        #тут есть баг, если лог с расширением .gz, потому в name
        # имя попадает без расширения
        now = datetime.strftime(datetime.now(), '%Y%m%d')
        log_now = 'nginx-access-ui.log-%s' % now
        with gzip.open(os.path.join(config['LOG_DIR'], log_now), 'w'):
            pass
        last_log = latest_log_get(config['LOG_DIR'])
        self.assertEqual(last_log.name, log_now)
        self.assertEqual(last_log.path, os.path.realpath(config['LOG_DIR']+ '/'))
        self.assertEqual(last_log.creation_date, datetime.strftime(datetime.now(), '%d.%m.%Y'))
        self.assertEqual(last_log.extention, None)

    def test_log_name_endwith_as_plain_text(self):
        """тест: что вернеться последний лог как plain text"""
        log_file = 'nginx-access-ui.log-%s' % self.random_date_gen(
                start='01.01.2017',
                end='04.05.2019')
        with open(os.path.join(config['LOG_DIR'], log_file), 'w'):
            pass
        last_log = latest_log_get(config['LOG_DIR'])
        self.assertEqual(last_log.extention, None)

    def test_log_name_endwith_gz(self):
        """тест: что  вернеться последний лог как архив .gz"""
        log_file = 'nginx-access-ui.log-%s.gz' % self.random_date_gen(
                start='01.01.2017',
                end='04.05.2019')
        with gzip.open(os.path.join(config['LOG_DIR'], log_file), 'w'):
            pass
        last_log = latest_log_get(config['LOG_DIR'])
        self.assertEqual(last_log.extention, '.gz')

    def test_log_name_not_return_bz2_extention(self):
        """тест: что ф-ция поиска свежего лога не возвращает .bz2"""
        log_file1 = 'nginx-access-ui.log-%s.gz' % self.random_date_gen(
            start='01.01.2017',
            end='04.05.2019')
        with gzip.open(os.path.join(config['LOG_DIR'], log_file1), 'w'):
            pass
        log_now = 'nginx-access-ui.log-%s.bz2' % datetime.strftime(datetime.now(), '%Y%m%d')
        with gzip.open(os.path.join(config['LOG_DIR'], log_now), 'w'):
            pass
        last_log = latest_log_get(config['LOG_DIR'])
        self.assertNotEqual(last_log.extention, '.bz2')


if __name__ == "__main__":
        unittest.main()