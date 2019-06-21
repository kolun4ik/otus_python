import os
import shutil
import random
from datetime import datetime, timedelta
from unittest import TestCase
from log_analyzer import config


class FunctionalTest(TestCase):
    """функциональный тест"""

    @classmethod
    def setUpClass(cls):
        """Установка, единажды"""
        # Временная директория для тестов
        config['LOG_DIR'] = '../log_'
        if not os.path.exists(config['LOG_DIR']):
            os.mkdir(config['LOG_DIR'])

    @classmethod
    def tearDownClass(cls):
        """Демонтаж"""
        if os.path.exists(config['LOG_DIR']):
            shutil.rmtree(config['LOG_DIR'])
            # pass

    def tearDown(self):
        """Установка для каждого теста"""
        if os.path.isdir(config['LOG_DIR']):
            for file in os.listdir(config['LOG_DIR']):
                file_path = os.path.join(config['LOG_DIR'], file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(e)

    def random_date_gen(self, start, end):
        """Генератор произвольной даты в диапазоне от start до end.
            Вызов: random_date_gen(start='01.01.2017', end='04.30.2019')"""
        utime1 = datetime.strptime(str(start), '%d.%m.%Y')
        utime2 = datetime.strptime(str(end), '%d.%m.%Y')
        delta = utime2.timestamp() - utime1.timestamp() # получили секунды
        random_date = utime1 + timedelta(seconds=random.randrange(delta))
        return random_date.strftime('%Y%m%d')


if __name__ == "__main__":
        unittest.main()