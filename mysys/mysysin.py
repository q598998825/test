# coding=utf-8
from mysocket import *
from mymsg import *
import logging, os

def Serverfunc(serv,sock,data):
    logging.debug(data)
    serv.resoponse(sock,"12345654987".encode())

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

    mysocket1 = mysocket()
    socket1 = mysocket1.sockInit(port=9090,IsClient =False)
    if (socket1 is None):
        logging.error("分配失败")
    else:
        logging.debug("链接成功")
        mysocketServerPool1 = mysocketServerPool()
        mysocketServerPool1.addSocket(socket1,Serverfunc)
        mysocketServerPool1.run()
    pass

def Proc(msg):
    pass

def myMsgInit():
    mymsg1 = mymsg(123,456)
    return 0
