import random
import string
import urllib.request

import time
from urllib import parse

import requests

from com import utils


def get_data(params, ip=None):
    count = 0
    url = parse.quote(utils.host + params, string.printable, 'gbk')
    while 1:
        if count > 6:
            page = ''
            break
        count = count + 1
        response = requests.get(url, timeout=100)
        print(response.status_code)
        if response.status_code == 200:
            page = response.text
            page = page.encode('utf-8')
            print(page)
            break
        else:
            print(params + '----connect failed status_code:' + response.status_code)
            time.sleep(random.randint(20, 40))
        # try:
        #     if ip:
        #         proxies = {'http': ip}
        #         opener = urllib.request.FancyURLopener(proxies)
        #         response = opener.open(url)
        #     else:
        #         response = requests.get(url, timeout=100)
        #     print(response.status_code)
        #     if response.status_code == 200:
        #         page = response.text
        #         page = page.encode('utf-8')
        #         print(page)
        #         break
        #     else:
        #         print(params + '----connect failed status_code:' + response.status_code)
        #         time.sleep(random.randint(20, 40))
        #     #     response = urllib.request.urlopen(utils.host + params, timeout=100)
        #     # if response.getcode() == 200:
        #     #     page = response.read()
        #     #     page = page.decode('gbk').encode('utf-8')
        #     #     break
        # except Exception as e:
        #     print(params + '----connect failed:' + str(e))
        #     time.sleep(random.randint(20, 40))
    return page


def post_data(name):
    while 1:
        data = {
            'domain': '',
            'blname': name.encode('gbk'),
            'bladdr': '',
            'prname': '',
            'Submit2222': '提交查询'.encode('gbk')
        }
        data = parse.urlencode(data).encode('gbk')
        try:
            response = urllib.request.urlopen(utils.host + 'xmqk.asp', data, 100)
            if response.getcode() == 200:
                page = response.read()
                page = page.decode('gbk').encode('utf-8')
                break
        except Exception as e:
            print('post_data connect failed:' + str(e))
            time.sleep(random.randint(20, 60))
    return page


def test_data(file_path):
    file_object = open(file_path, 'r', encoding='utf-8')
    page = ''
    try:
        page = file_object.read()
    except Exception as e:
        print('Exception:' + str(e))
    finally:
        file_object.close()
    return page

