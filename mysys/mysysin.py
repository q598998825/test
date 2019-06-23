# coding=utf-8
from mysocket import *
from mymsg import *
from mymsgmng import *
import logging, os
from mycomm import *

g_MySysInInitFunc = [{"name": "myMsgInit","notes": "","init": "myMsgInit","proc":None}]


def Init(Mysys):
    global g_MySysInInitFunc
    for map1 in g_MySysInInitFunc:
        try:
            if(0 > eval(map1["init"])()):
                logging.error("%s failed!!!"%map1["name"])
                os._exit(1)
            if False == strIsNone(map1["proc"]):
                Mysys.addProc(map1["name"],eval(map1["proc"]))
        except Exception as e:
            logging.error("基础函数[%s]初始化异常：%s" % (map1["name"], e.__str__()))
            os._exit(1)
    return 0

def myMsgInit():
    mymsgMng1 = mymsgMng()
    mymsgMng1.Init("127.0.0.1",9091,123)
    mymsgMng2 = mymsgMng()
    print(mymsgMng1,mymsgMng2)
    return 0
