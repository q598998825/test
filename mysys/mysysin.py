# coding=utf-8
from mysocket import *
from mymsg import *

def Serverfunc(serv,sock,data):
    print(data)
    serv.resoponse(sock,"12345654987")

def Init():
    mysocket1 = mysocket()
    socket1 = mysocket1.sockInit(port=9090,IsClient =False)
    if (socket1 is None):
        print("分配失败")
    else:
        print("链接成功")
        mysocketServerPool1 = mysocketServerPool()
        mysocketServerPool1.addSocket(socket1,Serverfunc)
        mysocketServerPool1.run()
    pass

def Proc(msg):
    pass
