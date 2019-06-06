# coding=utf-8
from mypthread import *
from mysocket import *
import logging
class mymsg():
    pass
class mymsgMng():
    def __init__(self):
        logging.debug("mymsg Init")
    def __del__(self):
        logging.debug("mymsg del")

    def Init(self,ip,port,id):
        #初始化环境用
        if(0 < self.registerServ(ip,port,id)):
            #注册失败
            if(0 < self.initServer(ip,port,id)):
                #生成服务失败
                logging.error("无法连接服务也无法作为服务启动(ip[%s],port[%s],id[%s])"%(ip,port,id))
                return -1


    def registerServ(self,ip,port,id):
        mysocket1 = mysocket()
        socket1  = mysocket1.sockInit(ip = ip,port =port)
        if (socket1 is None):
            logging.error("连接失败")

        return 0

    def initServer(self,ip,port,id):
        mysocket1 = mysocket()
        socket1 = mysocket1.sockInit(ip = ip,port=port, IsClient=False)
        if (socket1 is None):
            logging.error("分配失败")
        else:
            logging.debug("链接成功")
            mysocketServerPool1 = mysocketServerPool()
            mysocketServerPool1.addSocket(socket1, self.Serverfunc)
            mysocketServerPool1.run()
        return 0

    def NativeCall(self,req,rsp):
        return 0

    def register(self,Func):
        return 0

    def Serverfunc(self, serv, sock, data):
        logging.debug(data)
        serv.resoponse(sock, "12345654987".encode())
