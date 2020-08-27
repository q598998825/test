import logging,socket,time
from myCommDM import *


class vpro_rule:
    def __init__(self):
        comm_param1 = comm_param()
        self.startKey = comm_param1.GetResult(comm_param1.useDefaultSql("getValue", "VSCRIPT_STARTKEY"))[0]["VALUE"]
        self.endKey = comm_param1.GetResult(comm_param1.useDefaultSql("getValue", "VSCRIPT_ENDKEY"))[0]["VALUE"]
        self.tab = comm_param1.GetResult(comm_param1.useDefaultSql("getValue", "VSCRIPT_TAB"))[0]["VALUE"]
        self.ruleMap={""}


    def socket(self,str):
        #获取参数
        tmpMap = self.socketGetVar(str)
        #初始化
        s=self.socketInit(tmpMap["socketType"],tmpMap["servIp"],tmpMap["servPort"])
        if s == None:
            logging.error("socket 初始化异常")
            exit(-1)
        #处理任务列表
        tasklist = tmpMap["tasklist"]
        retMap = {}
        for task in tasklist:
            self.socketExec(s,retMap,task)
        return 0

    def socketExec(self,s,retMap,str):
        # 获取规则函数名
        tmpMap = self.GetVar(str, self.startKey, self.tab, 0)
        funcname = tmpMap["0"]
        if (funcname == ""):
            logging.error("socketExec has not rule Func")
            exit
        endindex = tmpMap["1"]
        # 获取规则处理对象
        tmpstr = str[endindex + 1:-len(self.endKey)]
        # 处理
        ret = eval("self." + funcname)(s,retMap,tmpstr)

    def accecpt(self,ServSock,retMap,str):
        logging.debug('got connected begin')
        cs, addr = ServSock.accept()
        logging.debug('got connected from %s:%s'%(addr[0],addr[1]))
        retMap[str]=cs


    def recv(self,ServSock,retMap,str):
        cs = retMap[str]
        rb = cs.recv(1024)
        logging.debug('recv buf %s'% rb)
        retMap["RecvBuf"] =rb

    def send(self,ServSock,retMap,str):
        tmpMap = self.GetVar(str,"",self.tab,0)
        sockKey = tmpMap["0"]
        if sockKey == "":
            logging.error('send data getSocket key failed. ', str)
            exit(-1)
        cs = retMap[sockKey]
        data = str[tmpMap["1"]+1:]
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
        #获取socket类型
        tmpMap = self.GetVar(str, "", self.tab, 0)
        socketType = tmpMap["0"]
        if(socketType != "UDP" and socketType != "TCP"):
            logging.error("socket 无法获取TCP或者UDP参数")
            exit(-1)
        #获取服务ip
        endIndex = tmpMap["1"]
        tmpMap = self.GetVar(str, self.tab, self.tab, endIndex)
        servIp = tmpMap["0"]
        if (servIp == ""):
            logging.error("socket 无法获取服务ip")
            exit(-1)
        #获取服务端口
        endIndex = tmpMap["1"]
        tmpMap = self.GetVar(str, self.tab, self.tab, endIndex)
        servPort = tmpMap["0"]
        if (servPort == ""):
            logging.error("socket 无法获取服务端口")
            exit(-1)

        #获取任务列表
        endIndex = tmpMap["1"]
        tasklist = []
        map = []
        index = 0
        tmpstr = str[endIndex:]

        index = self.GetTaskList_in(map, index, tasklist, tmpstr)
        while (index != -1):
            index = self.GetTaskList_in(map, index, tasklist, tmpstr)

        return {"socketType":socketType,"servIp":servIp,"servPort":servPort,"tasklist":tasklist}

    def exec(self,tmpvscript,file_context):
        #初始化数据
        self.InitData(tmpvscript,file_context)

        # 加载任务
        self.GetTaskList()

        #处理任务
        self.DealTaskList()

    # ********************************************** 下面为标准一般不动的函数 ******************************

    def InitData(self,tmpvscript,file_context):
        self.vscript = tmpvscript
        self.file_context = file_context
        self.tasklist = []

    def GetTaskList(self):
        map = []
        index = 0
        index = self.GetTaskList_in(map,index,self.tasklist,self.file_context)
        while(index != -1):
            index = self.GetTaskList_in(map, index,self.tasklist,self.file_context)


    def GetTaskList_in(self,map,index,tasklist,file_context):

        tmpIndex = file_context.find(self.startKey, index)
        tmpEnd = file_context.find(self.endKey, index)

        if (tmpIndex != -1 and
                tmpIndex < tmpEnd):
            map.append(tmpIndex)
            return self.GetTaskList_in(map, tmpIndex + len(self.startKey),tasklist,file_context)
        elif (tmpEnd != -1):
            tmpStart = map.pop()
            tmpIndex = tmpEnd + len(self.endKey)
            if len(map) == 0:#只有最外层作为任务处理
                tmp = file_context[tmpStart:tmpIndex]
                tasklist.append(tmp)
        return tmpIndex

    def DealTaskList(self):
        i = 1
        for task in self.tasklist:
            logging.debug("执行任务 task[%d]" % i)
            # 获取规则函数名
            tmpMap = self.GetVar(task, self.startKey, self.tab, 0)
            funcname = tmpMap["0"]
            if (funcname == ""):
                logging.error("DealTaskList has not rule Func")
                continue
            endindex = tmpMap["1"]
            # 获取规则处理对象
            tmpstr = task[endindex+1:-len(self.endKey)]
            # 处理
            ret = eval("self." + funcname)(tmpstr)

            if (ret != 0):
                logging.error("DealTaskList rule Func Dealing Failed")
                return


    def GetVar(self,str,startKey,endKey,index):
        tmpStart =0
        if(startKey != ""):
            tmpStart = str.find(startKey, index)
        tmpEnd = str.find(endKey, tmpStart + len(startKey))
        if (tmpStart == -1 or tmpEnd == -1):
            logging.error("GetVar 获取变量失败，startKey[%s],endKey[%s],index[%s]\nstr[%s]"%(startKey,endKey,index,str))
            return {"0": "", "1": -1}

        tmp = str[tmpStart + len(startKey):tmpEnd]
        return {"0":tmp,"1":tmpEnd}


    def socketSleep(self,ServSock,retMap,str):
        logging.error("socketSleep %s"%str)
        time.sleep(int(str))
