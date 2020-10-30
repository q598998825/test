# coding=utf-8
import os
from wsgiref.simple_server import make_server
'''
循环安装脚本
'''
install_array = {"jieba":["pip install jieba"]}

'''
test123
'''
for install_type in install_array:
    try:
        eval("import %s"%install_type)
    except:
        for cmd in install_array[install_type]:
            os.system(cmd)
