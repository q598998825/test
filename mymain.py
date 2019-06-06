# coding=utf-8
from mysys.mysys import *
import time, logging

def logInit():
    #因为此函数之前不能有logging的调用故放此处
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    return 0

if __name__ == '__main__':
    logInit()
    mysys1 = mysys()
    mysys1.InitEnv()
    while True:
        time.sleep(100000)
