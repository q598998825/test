# coding=utf-8
from mypthread import *
from mysocket import *
import logging
from mysingleton import *

def myMsgMngInit():
    mymsgMng1 = mymsgMng()
    mymsgMng1.Init("127.0.0.1",9091,123)
    mymsgMng2 = mymsgMng()
    print(mymsgMng1,mymsgMng2)
    return 0

@singleton
class mymsgMng():
    func_pool = {} #存储okcpde用
    ids_pool = {}   #存储服务用
    Servip = ""     #提供给opcode的服务ip
    Servport = 0    #提供给opcode的

    def Init(self,ip,port,id):
        #初始化环境用
        if(0 > self.registerServ(ip,port,id)):
            #注册失败
            if(0 > self.initServer(ip,port,id)):
                #生成服务失败
                logging.error("无法连接服务也无法作为服务启动(ip[%s],port[%s],id[%s])"%(ip,port,id))
                return -1
        self.initOpcodeServer(id)

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
            mysocketServerPool1.addSocket(socket1, self.registServerfunc,self.registCloseFunc)
            mysocketServerPool1.run()
        return 0

    def initOpcodeServer(self,id):
        mysocket1 = mysocket()
        socket1 = mysocket1.sockInit(IsClient=False)
        self.Servip,self.Servport = socket1.sock.getsockname()
        logging.debug("%s,%d"%(self.Servip,self.Servport))
        mypthread1 = mypthread(self.Serverfunc,self)
        mypthread1.start()

    def register(self,opcode,Func):
        if opcode in self.func_pool:
            logging.error("此opcode[%s]已注册，不能重复注册"%opcode)
            return -1
        self.func_pool[opcode] = Func
        return 0

    def Serverfunc(self, arg):
        #消息分类处理
        logging.debug(arg)

    def CloseFunc(self,serv,sock,errcode,errinfo):
        print("closefunc",errcode,errinfo)

    def registServerfunc(self, serv, sock, data):
        #消息分类处理
        logging.debug(data)

    def registCloseFunc(self,serv,sock,errcode,errinfo):
        print("closefunc",errcode,errinfo)
