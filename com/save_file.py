import os


def save_file_data(file_name, file_content):
    #    注意windows文件命名的禁用符，比如 /
    path = os.path.abspath(os.path.dirname(os.getcwd())) + '\\' + file_name
    if not os.path.exists(path):
        os.mkdir(path)

    with open(path + '\\' + file_name.replace('/', '_') + ".txt", "ab+") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(bytes((file_content + '\n'), encoding='utf-8'))
