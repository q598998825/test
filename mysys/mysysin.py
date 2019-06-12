# coding=utf-8
from mysocket import *
from mymsg import *
from mymsgmng import *
import logging, os

g_MySysInInitFunc = ["myMsgInit"]

def Init():
    global g_MySysInInitFunc
    for func in g_MySysInInitFunc:
        try:
            if(0 > eval(func)()):
                logging.error("%s failed!!!"%func)
                os._exit(1)
        except Exception as e:
            logging.error("基础函数[%s]初始化异常：%s" % (func, e.__str__()))
            os._exit(1)
    return 0

def Proc(msg):
    pass

def myMsgInit():
    mymsgMng1 = mymsgMng()
    mymsgMng1.Init("127.0.0.1",9091,123)
    mymsgMng2 = mymsgMng()
    print(mymsgMng1,mymsgMng2)
    return 0
