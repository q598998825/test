# coding=utf-8
from mymsgmng import *
import logging, os
from mycomm import *
from mytimermng import *
from globalConfig import *
from mydatabasemng import *
from myCommDM import *

g_MySysInInitFunc = [{"name": "myBaseConfigInit","notes": "基础配置","init": "globalConfigInit","proc":None},
                    {"name": "myDatabase","notes": "数据库初始化","init": "myDataBaseInit","proc":None},
                    {"name": "myMsgInit","notes": "消息系统","init": "myMsgMngInit","proc":None},
                    {"name": "Timer","notes": "定时器","init": "myTimerMngInit","proc":"myTimerMngProc"}]


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
            logging.error("基础函数[%s]初始化异常：%s\n%s" % (map1["name"], e.__str__(),traceback.format_exc()))
            os._exit(1)
    return 0
