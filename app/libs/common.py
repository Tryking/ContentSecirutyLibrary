import inspect
import json
import logging
import logging.handlers
import os
import random
import socket
import re
import time

import requests
from fake_useragent import UserAgent

PROXY_URL = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&pack=23790&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='


def init_log(console_level, file_level, logfile):
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s')
    logging.getLogger().setLevel(0)
    console_log = logging.StreamHandler()
    console_log.setLevel(console_level)
    console_log.setFormatter(formatter)
    file_log = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024 * 1024 * 50, backupCount=10,
                                                    encoding='UTF-8')
    file_log.setLevel(file_level)
    file_log.setFormatter(formatter)
    logging.getLogger().addHandler(file_log)
    logging.getLogger().addHandler(console_log)


def write_file_log(msg, __module='', level='error'):
    filename = os.path.split(__file__)[1]
    if level == 'debug':
        logging.getLogger().debug('File:' + filename + ', ' + __module + ': ' + msg)
    elif level == 'warning':
        logging.getLogger().warning('File:' + filename + ', ' + __module + ': ' + msg)
    else:
        logging.getLogger().error('File:' + filename + ', ' + __module + ': ' + msg)


def get_current_func_name():
    return inspect.stack()[1][3]


def get_random_str(str_len):
    content = 'abcdefghijklmnopqrstuvwxyz1234567890'
    min_index = 0
    max_index = len(content) - 1
    output = []
    for i in range(str_len):
        index = random.randint(min_index, max_index)
        output.append(content[index:index + 1])
    output = ''.join(output)
    return output


def handle_xpath_str(xpath_result):
    """
    处理xpath字符串的结果，当没有匹配到对应的xpath时，给xpath结果添加一个空字符串元素
    """
    if len(xpath_result) > 0:
        return xpath_result
    else:
        xpath_result.append('')
        return xpath_result


def get_clean_data(original_data):
    """
    将原始字符串的中间空格和两边空格去掉
    """
    return re.sub('\s', '', original_data).replace(':', '').replace('：', '')


def get_standard_file_name(original_file_name):
    """
    获取标准文件名（去除特殊符号）
    :param original_file_name:
    :return:
    """
    special_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in special_chars:
        original_file_name = original_file_name.replace(char, '')
    return original_file_name.strip()


def remove_bracket(original_str):
    """
    移除字符串中括号以及之间的内容

    https://dl.phncdn.com/pics/albums/006/542/202/102689682/(m=bKaz0Np)(mh=waVqbkwB3QiO7vdV)original_102689682.jpg
    :param original_str: 原始字符串
    :return: 修改后的字符串
    """
    if '(' in original_str and ')' in original_str:
        start = original_str.split('(', maxsplit=1)
        end = original_str.rsplit(')', maxsplit=1)
        return start[0] + end[len(end) - 1]
    else:
        return original_str


def get_proxy():
    """
    获取代理
    :return:
    """
    proxys = [None]
    return random.choice(proxys)


def test_ip_available(proxy_ip, url='https://www.baidu.com'):
    """
    测试代理IP是否可用
    :param ip:
    :return:
    """
    try:
        proxies = {"http": proxy_ip, "https": proxy_ip}
        r = requests.get(url=url, headers=get_headers(), timeout=5,
                         proxies=proxies)
        if r.ok:
            return True
        else:
            return False
    except Exception as e:
        return False


def get_available_ip_proxy():
    """
    获取可用IP（从IP池获取，并测试是否可用）
    :return:
    """
    try:
        proxys = requests.get(PROXY_URL).text
        write_file_log('获取代理：' + str(proxys))
        if judge_legal_ip(proxys.strip(), contains_port=True):
            proxy = 'http://%s' % (proxys.strip())
            return proxy
        else:
            return None
    except Exception as e:
        return None


def get_udpate_time():
    """
    获取更新时间
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_num_from_str(str):
    """
    从给定的字符串中提取出数字
    """
    nums = re.findall(r"\d+", str)
    return int(''.join(nums))


def judge_legal_ip(one_str, contains_port=False):
    """
    正则匹配方法
    判断一个字符串是否是合法IP地址
    """
    try:
        if contains_port:
            ip_port = one_str.split(':')
            if len(ip_port) == 2:
                compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
                if compile_ip.match(ip_port[0]):
                    # TODO：判断端口是否合法
                    return True
                else:
                    return False
            else:
                return False
        compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if compile_ip.match(one_str):
            return True
        else:
            return False
    except Exception as e:
        raise e


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_search_director_set(directors_str):
    """
    从导演字符串中获取导演列表（多个导演以 | 分割）
    """
    director_set = set()
    directors = directors_str.split('|')
    for director in directors:
        director_set.add(director.strip())
    return director_set


def is_valid_url(url):
    """
    判定链接是否合法
    """
    if re.match(r'^https?:/{2}\w.+$', url):
        return True
    else:
        return False


# 获取前几天的日期字符串(包含年)
def get_before_date(before_day=None):
    # 默认获取昨天的
    if before_day is None:
        before_day = 1
    return time.strftime("%Y-%m-%d", time.localtime(time.time() - 3600 * 24 * before_day))
