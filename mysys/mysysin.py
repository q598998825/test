# coding=utf-8
from mysocket import *
from mymsg import *
import logging

def Serverfunc(serv,sock,data):
    logging.debug(data)
    serv.resoponse(sock,"12345654987".encode())

def logInit():
    logging.basicConfig(level=logging.DEBUG)
    return -1



g_MySysInInitFunc = [logInit]

def Init():
    global g_MySysInInitFunc
    for func in g_MySysInInitFunc:
        if(0 > func()):
            logging.error("%s failed!!!"%str(func))
            exit(1)

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
