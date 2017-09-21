import random
import urllib.request
import re
import time

list_title = []
list_content = []

####################################################################################
# 已废弃############################################################################
####################################################################################


def save_html(file_name, file_content):
    #    注意windows文件命名的禁用符，比如 /
    with open(file_name.replace('/', '_') + ".html", "wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(file_content)


def save_zone(key, content):
    with open('19.txt', "a+") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(key + ":" + content + "\n")


def get_zone(title,html):
    html = html.decode('gbk')
    res_tr = r'<tr.*?>.*?预测面积(.*?)</tr>'
    m_tr = re.findall(res_tr, html, re.S | re.M)
    for line in m_tr:
        res_td = r'<td.*?>(.*?)</td>'
        m_td = re.findall(res_td, line, re.S | re.M)
        for nn in m_td:
            nn1 = nn.replace('\t', '').replace('\n', '').replace(' ', '')
            print("预测面积:" + nn1)
            save_zone(title, nn1)


def get_html_content():
    file_object = open('19.html', 'r', 4096, 'utf-8')
    try:
        html = file_object.read()
        # 去掉换行和空格
        html = html.replace('\n', '').replace(' ', '')
    finally:
        file_object.close()
    print(html)
    res = r'房型.*?<a.*?>(.*?)</a>'
    values = re.findall(res, html, re.S | re.M)
    is_one = True
    for value in values:
        if value.find("二层卫生间") > -1:
            is_one = False
        if is_one:
            list_title.append("19-1-" + value)
        else:
            list_title.append("19-2-" + value)
    res = r'房型.*?<ahref=\'(.*?)\'target.*?</a>'
    values1 = re.findall(res, html, re.S | re.M)
    for value in values1:
        list_content.append(value)


def get_html(url):
    get_html_content()
    size = len(list_title)
    print(".....总共数据有：" + str(size))
    for i in range(size):
        print(">>>>开始" + list_title[i])
        while True:
            try:
                # 处理得到的网页
                if list_content[i].find('00000000') > 0:
                    break
                html = urllib.request.urlopen(url + list_content[i]).read()
                save_html("18_" + str(list_title[i]), html)
                get_zone(list_title[i], html)
                print(list_title[i] + "成功<<<<<<")
                break
            except Exception as err:
                print(list_title[i] + "出错:" + str(err))
                time.sleep(random.randint(20, 60))


print("总开始.....")
get_html("http://119.97.201.28:8087/")
print("总结束")
