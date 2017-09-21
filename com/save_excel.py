import xlwt
from datetime import datetime

from com import utils

list_result = []


def get_info(line):
    print(line.split(utils.split_str))
    list_t = line.split(utils.split_str)
    list_result.append(list_t)


def get_data(file_path, file_name):
    list_result.append(['楼号', '面积', '价格'])
    file_object = open(file_path + file_name + '.txt', 'r', 4096, 'utf-8')
    while 1:
        line = file_object.readline()
        if not line:
            break
        else:
            # 去掉换行和空格
            line = line.replace(' ', '').replace('\n', '')
            if len(line) <= 0:
                continue
            print(line)
            get_info(line)
    file_object.close()


def save(file_name, file_path):
    get_data(file_path, file_name)
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', True)
    # 获取当前日期，得到一个datetime对象如：(2016, 8, 9, 23, 12, 23, 424000)
    today = datetime.today()
    # 将获取到的datetime对象仅取日期如：2016-8-9
    today_date = datetime.date(today)
    # 遍历result中的没个元素。
    print(list_result)
    print(len(list_result))
    for i in range(len(list_result)):
        # 对result的每个子元素作遍历，
        for j in range(len(list_result[i])):
            # 将每一行的每个元素按行号i,列号j,写入到excel中。
            sheet.write(i, j, list_result[i][j])
    # 以传递的name+当前日期作为excel名称保存。
    wbk.save(file_path + file_name + str(today_date) + '.xls')


# 主程序开始
# save()
