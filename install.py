# coding=utf-8
import os

install_array = {"spacy":['pip install spacy','pip install path/en_core_web_lg-2.0.0.tar.gz']}

str = input("请输入安装类型：");

if str != "all":
    if str not in install_array:
        print("无此类型的安装命令")
    for cmd in  install_array[str]:
        os.system(cmd)
else:
    for install_type in install_array:
        for cmd in install_array[install_type]:
            os.system(cmd)