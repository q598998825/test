# coding=utf-8
from mypthread import *
from mysocket import *
import logging

class mymsgMng():
    def Init(self,ip,port,id):
        #初始化环境用
        if(0 > self.registerServ(ip,port,id)):
            #注册失败
            if(0 > self.initServer(ip,port,id)):
                #生成服务失败
                logging.error("无法连接服务也无法作为服务启动(ip[%s],port[%s],id[%s])"%(ip,port,id))
                return -1


    def registerServ(self,ip,port,id):
        mysocket1 = mysocket()
        try:
            socket1  = mysocket1.sockInit(ip = ip,port =port)
            if (socket1 is None):
                logging.error("连接失败")
                return -1
        except Exception as e:
            logging.error("连接失败[%s]"%e.__str__())
            return -1
        return 0

    def initServer(self,ip,port,id):
        mysocket1 = mysocket()
        try:
            socket1 = mysocket1.sockInit(ip = ip,port=port, IsClient=False)
        except Exception as e:
            logging.error("分配服务失败[%s]"%e.__str__())
            return -1
        if (socket1 is None):
            logging.error("分配服务失败")
            return -1
        else:
            logging.debug("分配服务成功")
            mysocketServerPool1 = mysocketServerPool()
            mysocketServerPool1.addSocket(socket1, self.Serverfunc)
            mysocketServerPool1.run()
        return 0

    def register(self,Func):
        return 0

    def Serverfunc(self, serv, sock, data):
        logging.debug(data)
        serv.resoponse(sock, "12345654987".encode())
