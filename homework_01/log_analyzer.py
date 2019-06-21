# -*- coding: utf-8 -*-
import os
import sys
import logging
import argparse
import json
import re
import gzip
import datetime
from string import Template
from collections import namedtuple, defaultdict, OrderedDict, Counter


config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"}

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';


regexp = re.compile(b'''(?:\S+)\s+(?:\S+)\s+(?:\S+)\s+\[(?:.*?)\]\s+"\S+ (?P<request>.*?) \S+"\s+(?:\d+)\s+(?:\d+)\s+"(?:.*?)"\s+"(?:.*?)"\s+"(?:.*?)"\s+"(?:.*?)"\s+"(?:.*?)"\s+(?P<req_time>\d+\.\d+)''')

def median(list_num):
    # Вычисляем медиану, число, характеризубщее выборку.
    # Это такое число выборки, что ровно половина из элементов
    # выборки больше него, а оставшая часть меньше.
    # (предварительно выборка упорядочивается по возрастанию)
    r = len(list_num)
    if r < 1:
        return None
    if r % 2 == 1:
        return sorted(list_num)[r//2]
    else:
        return sum(sorted(list_num)[r//2 -1:r//2 + 1]) / 2.0


def logger_init():
    """Logging configure and initialization"""
    if os.path.exists(config['LOG_DIR']):
        log_file = os.path.join(config['LOG_DIR'],'log_analyzer.log')
    else:
        log_file = None
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(message)s",
                       datefmt="%Y.%m.%d %H:%M:%S",
                       level=logging.DEBUG,
                       filename=log_file)
    # stdout in console
    console = logging.StreamHandler()
    logger = logging.getLogger(__name__)
    logger.addHandler(console)
    logger.info("Programm log_analazer.py started")
    return logger


def cli_parser():
    """ Command line interface parser initialisation"""
    cli_parser = argparse.ArgumentParser(description='Log analyzer application for NGINX services')
    cli_parser.add_argument('-c', '--config', default='./config.py')
    cli_parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    return cli_parser.parse_args()


def read_param(filename):
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


def latest_log_get(path_to_dir):
    """Function get latest file with log Nginx
    for path and return namedtuple()"""
    if os.path.isdir(path_to_dir):
        latest_log, latest_ext = None, None
        search_pattern = re.compile(r'^nginx-access-ui\.log-(\d{8})(\.gz)?$')
        log_object = namedtuple('Log', 'path name creation_date extention')
        for file_name in os.listdir(path_to_dir):
            log_file = search_pattern.match(file_name)
            if log_file:
                date, extention = log_file.groups()
                creaation_date = datetime.datetime.strptime(date, '%Y%m%d').date()
                if not latest_log or creaation_date > latest_log:
                    latest_log = creaation_date
                    latest_ext = extention
        if latest_log:
            return log_object(
                os.path.abspath(path_to_dir + '/'),
                'nginx-access-ui.log-' + latest_log.strftime("%Y%m%d"),
                latest_log.strftime('%d.%m.%Y'),
                latest_ext)
        else:
            raise IOError('File log Nginx not present in directory %s' % path_to_dir)
    else:
        raise IOError("Directory  %s not exists" % path_to_dir)


def parser_log_statistics(log_path, log_name):
    """Parsing log NGINX for calculate statistics"""
    total = error = 0
    log = os.path.join(log_path, log_name)
    raw_statistics = defaultdict(list)
    with gzip.open(log, 'rb') if log.endswith('.gz') \
        else open(log,'rb') as f_obj:
        # Побежали по строкам лога
        for line in f_obj:
            parsed_line = regexp.match(line)
            if parsed_line:
                total += 1
                raw_statistics[parsed_line.group('request').decode('utf-8')].append(float(parsed_line.group('req_time')))
            else:
                error += 1
    threshold = round(error * 100 / (total + error))
    if threshold > 30:
        raise OverflowError('The threshold for reading errors exceeds the specified value (30%)')
    return raw_statistics


def calculate_statistics(dataset, size=config['REPORT_SIZE']):
    """Calculate statistics for report. Return REPORT_SIZE Urls
    with the longest total processing time (time_sum)"""
    processed_data = list()
    total_url = total_time_req = 0
    for _, c in dataset.items():
        total_url += len(c)
        total_time_req += sum(c)

    for url, data in dataset.items():
        count = len(data)
        time_sum = sum(data)
        time_avg = time_sum / count
        time_med = median(data)
        count_perc = count * 100 / total_url
        time_perc = time_sum * 100 / total_time_req

        line = {
            'count': count,
            'time_avg': round(time_avg,3),
            'time_max': round(max(data),3),
            'time_sum': round(time_sum,3),
            'url': url,
            'time_med': round(time_med,3),
            "time_perc": round(time_perc,3),
            "count_perc": round(count_perc,3)
        }
        processed_data.append(line)
    return sorted(
        processed_data,
        key=lambda data: data['time_sum'],
        reverse=True)[:config['REPORT_SIZE']]

def generate_report(dir_reports, data):
    """Genereate report file in directory ./reports used template report.html"""
    if os.path.isdir(dir_reports):
        with open(os.path.join(dir_reports, 'report.html'),'r', encoding='utf-8') as template_report:
            now = datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d')
            with open(os.path.join(dir_reports, f'report-{now}.html'), 'w', encoding='utf-8') as report:
                render = Template(template_report.read())
                report.write(render.safe_substitute(table_json=data))
                with open(os.path.join(dir_reports,'.tmp.json'), 'w', encoding='utf-8') as tmp:
                    json.dump(now, tmp)
    else:
        raise IOError("Report directory %s does not exist" % dir_reports)


def main():
    """Main function log_analizer.py"""
    try:
        logger = logger_init()
        args = cli_parser()
        new_config = read_param(args.config)
        config.update(new_config)
        tmp = os.path.join(config['REPORT_DIR'], '.tmp.json')
        # tmp_date = datetime.datetime.strptime(read_param(tmp), '%Y.%m.%d')
        if os.path.exists(tmp):
            if datetime.datetime.strptime(read_param(tmp), '%Y.%m.%d').date() == datetime.datetime.now().date():
                sys.exit('Log files have already been processed')
            else:
                latest_log = latest_log_get(config['LOG_DIR'])
                statistics = parser_log_statistics(latest_log.path, latest_log.name + latest_log.extention)
                data = calculate_statistics(statistics)
                generate_report(config['REPORT_DIR'], data)
        else:
            latest_log = latest_log_get(config['LOG_DIR'])
            statistics = parser_log_statistics(latest_log.path, latest_log.name + latest_log.extention)
            data = calculate_statistics(statistics)
            generate_report(config['REPORT_DIR'], data)

    except (IOError) as e:
        logger.warning(e)
        sys.exit(0)

    except (OverflowError) as e:
        logger.error(e)
        sys.exit(0)

    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("Programm log_analyzer.py finished")


if __name__ == '__main__':
    main()