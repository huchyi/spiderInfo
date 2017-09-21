# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用
import telnetlib
import threading

from bs4 import BeautifulSoup
import requests
import random

efficient_ip = []


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


# def get_random_ip(ip_list):
#     proxy_list = []
#     for ip in ip_list:
#         proxy_list.append('http://' + ip)
#     proxy_ip = random.choice(proxy_list)
#     proxies = {'http': proxy_ip}
#     return proxies


def test_ip(ip):
    try:
        print(ip)
        ip_str = ip.split(':')
        telnetlib.Telnet(ip_str[0], port=ip_str[1], timeout=20)
    except Exception as e:
        print('connect failed:' + str(e))
    else:
        efficient_ip.append('http://' + ip)
        print('success')


def get_efficient_ip(ip_list):
    threads = []
    for i in ip_list:
        thread = threading.Thread(target=test_ip, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()
    return efficient_ip


def ip_list():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    return get_efficient_ip(ip_list)


if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    print(ip_list)
    print(get_efficient_ip(ip_list))
    # proxies = get_random_ip(ip_list)
    # print(proxies)