# coding=utf-8
import logging,socket

class vpro_socket:
    def __init__(self):#子类统一初始化
        pass

    def socket(self,str):
        #获取参数
        tmpMap = self.socketGetVar(str)
        #初始化
        s=self.socketInit(tmpMap["socketType"],tmpMap["servIp"],tmpMap["servPort"])
        if s == None:
            logging.error("socket 初始化异常")
            exit(-1)
        #处理任务列表
        self.Data[self.SocketServerKey] = s #默认设置，为了统一处理
        tasklist = tmpMap["tasklist"]
        for task in tasklist:
            self.socketExec(task)
        return 0

    def socketExec(self,str):
        # 获取规则函数名
        tmpMap = self.GetVar(str, self.startKey, self.tab, 0)
        funcname = tmpMap["0"]
        if (funcname == ""):
            logging.error("socketExec has not rule Func")
            exit
        endindex = tmpMap["1"]
        # 获取规则处理对象
        tmpstr = self.FormatData(str[endindex + 1:-len(self.endKey)])
        # 处理
        ret = eval("self." + funcname)(tmpstr)

    def accecpt(self,str):
        logging.debug('got connected begin')
        ServSock = self.Data[self.SocketServerKey]
        cs, addr = ServSock.accept()
        logging.debug('got connected from %s:%s'%(addr[0],addr[1]))
        self.Data[str]=cs

    def recv(self,str):
        cs = self.Data[str]
        rb = cs.recv(1024)
        logging.debug('recv buf %s'% rb)
        self.Data["RecvBuf"] =rb

    def send(self,str):
        tmpMap = self.GetVarList(str)
        if len(tmpMap) <2:
            logging.error('send data getSocket key failed. ', str)
            exit(-1)
        sockKey = tmpMap[0]
        if sockKey == "":
            logging.error('send data getSocket key failed. ', str)
            exit(-1)
        cs = self.Data[sockKey]
        data = tmpMap[1]
        logging.debug('send buf %s' %data)
        cs.send(data.encode())

    def socketInit(self,type,ip,port):
        address = (ip, int(port))
        s = None
        if(type == "TCP"):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
            s.bind(address)
            s.listen(50)
        else:
            #暂不支持tcp以外的协议
            logging.error("socket 初始化异常")
            exit(-1)
        return s

    def socketGetVar(self,str):
        tmpMap = self.GetVarList(str)
        #获取socket类型
        socketType = tmpMap[0]
        if(socketType != "UDP" and socketType != "TCP"):
            logging.error("socket 无法获取TCP或者UDP参数")
            exit(-1)
        #获取服务ip
        servIp = tmpMap[1]
        if (servIp == ""):
            logging.error("socket 无法获取服务ip")
            exit(-1)
        #获取服务端口
        servPort = tmpMap[2]
        if (servPort == ""):
            logging.error("socket 无法获取服务端口")
            exit(-1)

        #获取任务列表
        tasklist = []
        map = []
        index = 0
        tmpstr = tmpMap[3]

        index = self._GetTaskList_in(map, index, tasklist, tmpstr)
        while (index != -1):
            index = self._GetTaskList_in(map, index, tasklist, tmpstr)

        return {"socketType":socketType,"servIp":servIp,"servPort":servPort,"tasklist":tasklist}
