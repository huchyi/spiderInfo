import random
import re

import os
import string
import urllib
from urllib import parse

import requests
from bs4 import BeautifulSoup
from com import net_work
from com import save_file
from com import save_excel
from com import utils
from com.proxy import get_ip

area_str = '预测面积'
price_str = '预售方案备案单价'
save_file_name = ''


# 解析商房信息
def analysis_shops_info(name, page):
    soup = BeautifulSoup(page, 'html.parser')
    list_1 = soup.find_all('td')
    list_t = []
    for value in list_1:
        soup = BeautifulSoup(str(value), 'html.parser')
        list_t.append(soup.td.string)
    point = 0
    dict_t = {}
    for value in list_t:
        if area_str in str(value):
            dict_t[area_str] = list_t[point + 1].replace('\n', '').replace(' ', '')
        elif price_str in str(value):
            dict_t[price_str] = list_t[point + 1].replace('\n', '').replace(' ', '')
        point = point + 1
    save_file.save_file_data(save_file_name,
                             name + utils.split_str + dict_t[area_str] + utils.split_str + dict_t[price_str])
    # print(name)
    # print(dict_t)


# 得到商房信息
def get_shops_info(name, params, ips):
    print('get_shops_info--------:' + params)
    if utils.is_debug:
        page = net_work.test_data('D:\pythonProjects\spiderDemo\yu_shui\\17\\17_test.html')
    else:
        count = 0
        while 1:
            if count > 5:
                ips = get_ip.ip_list()
                count = 0
            page = net_work.get_data(params, random.choice(ips))
            if page:
                break
            else:
                count = count + 1
    analysis_shops_info(name, page)


# 解析这栋楼的带商的信息
def analysis_floor_info(floor_num_name, page):
    soup = BeautifulSoup(page, 'html.parser')
    list_1 = soup.find_all('a')
    print(len(list_1))
    res = r'商</a>'
    list_data = []
    num = 1
    ips = get_ip.ip_list()
    for value in list_1:
        if len(re.findall(res, str(value))) > 0:
            soup = BeautifulSoup(str(value), 'html.parser')
            num_name = soup.a.string
            params = soup.a.get('href')
            print(num_name + '............:' + params)
            list_data.append(num_name)
            num2 = list_data.count(num_name)
            if num2 > num:
                num = num2
            get_shops_info(floor_num_name + '-' + str(num2) + '层-' + num_name, params, ips)


# 得到一栋楼的所有住户信息
def get_floor_info(floor_num_name, params):
    if utils.is_debug:
        page = net_work.test_data('D:\pythonProjects\spiderDemo\yu_shui\\19\\19.html')
    else:
        page = net_work.get_data(params)
    analysis_floor_info(floor_num_name, page)


# 分析楼列表的信息
def analysis_floor_list_info(page):
    soup = BeautifulSoup(page, 'html.parser')
    list_1 = soup.find_all('a')
    res = r'</span>'
    for value in list_1:
        if len(re.findall(res, str(value))) > 0:
            soup = BeautifulSoup(str(value), 'html.parser')
            floor_num_name = soup.span.string.replace('\n', '').lstrip().rstrip()
            params = soup.a.get('href')
            print('analysis_floor_list_info>>>>>>>>>>> ' + floor_num_name + ':' + params)
            get_floor_info(floor_num_name, params)


# 得到楼列表的信息
def get_floor_list_info(params):
    print('url:' + params)
    if utils.is_debug:
        page = net_work.test_data('D:\pythonProjects\spiderDemo\yu_shui\estate_list.html')
    else:
        page = net_work.get_data(params)
    analysis_floor_list_info(page)


# 解析地块信息
def analysis_area_info(page):
    soup = BeautifulSoup(page, 'html.parser')
    list_1 = soup.find_all('a')
    res = r'</span>'
    for value in list_1:
        if len(re.findall(res, str(value))) > 0:
            soup = BeautifulSoup(str(value), 'html.parser')
            value_v = soup.a.get('href')
            get_floor_list_info(value_v)


# 循环接口请求地块信息
def get_area_info(dict_list):
    print(dict_list)
    for key in dict_list:
        value = dict_list[key]
        print(key + ':' + value)
        if utils.is_debug:
            page = net_work.test_data('D:\pythonProjects\spiderDemo\yu_shui\estate_info.html')
        else:
            page = net_work.get_data(value)
        analysis_area_info(page)


# 解析搜索的结果
def analysis_estate(page):
    soup = BeautifulSoup(page, 'html.parser')
    list_1 = soup.find_all('a')
    dict_list = {}
    res = r'</span>'
    for value in list_1:
        if len(re.findall(res, str(value))) > 0:
            soup = BeautifulSoup(str(value), 'html.parser')
            key = soup.span.string
            value_v = soup.a.get('href')
            dict_list[key] = value_v
    get_area_info(dict_list)


# 根据名字搜索
def search_estate(name):
    # 全局变量重新赋值
    print("all start")
    global save_file_name
    save_file_name = name
    if utils.is_debug:
        page = net_work.test_data('D:\pythonProjects\spiderDemo\yu_shui\search_info.html')
    else:
        page = net_work.post_data(name)
    analysis_estate(page)
    path = os.path.abspath(os.path.dirname(os.getcwd())) + '\\' + name + '\\'
    save_excel.save(name, path)
    print("all end")


if __name__ == '__main__':
    net_work.get_data('3.asp?DengJh=阳1600080')
    # url = parse.quote(utils.host + '3.asp?DengJh=阳1600080', string.printable, 'gbk')
    # print(url)

