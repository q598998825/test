import logging,socket,time,re
from myCommDM import *


class vpro_rule:
    def __init__(self):
        comm_param1 = comm_param()
        self.startKey = comm_param1.GetResult(comm_param1.useDefaultSql("getValue", "VSCRIPT_STARTKEY"))[0]["VALUE"]
        self.endKey = comm_param1.GetResult(comm_param1.useDefaultSql("getValue", "VSCRIPT_ENDKEY"))[0]["VALUE"]
        self.tab = ','
        self.strltab = '{'
        self.strrtab = '}'
        self.ruleMap={""}
        self.Data={}
        self.SocketServerKey="ServerSock"


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

    def exec(self,tmpvscript,file_context):
        #初始化数据
        self.InitData(tmpvscript,file_context)

        # 加载任务
        self._GetTaskList()

        #处理任务
        self._DealTaskList()

    # ********************************************** 下面为标准一般不动的函数 ******************************

    def InitData(self,tmpvscript,file_context):
        self.vscript = tmpvscript
        self.file_context = file_context
        self.tasklist = []

    def _GetTaskList(self):
        map = []
        index = 0
        index = self._GetTaskList_in(map,index,self.tasklist,self.file_context)
        while(index != -1):
            index = self._GetTaskList_in(map, index,self.tasklist,self.file_context)


    def _GetTaskList_in(self,map,index,tasklist,file_context):

        tmpIndex = file_context.find(self.startKey, index)
        tmpEnd = file_context.find(self.endKey, index)

        if (tmpIndex != -1 and
                tmpIndex < tmpEnd):
            map.append(tmpIndex)
            return self._GetTaskList_in(map, tmpIndex + len(self.startKey),tasklist,file_context)
        elif (tmpEnd != -1):
            tmpStart = map.pop()
            tmpIndex = tmpEnd + len(self.endKey)
            if len(map) == 0:#只有最外层作为任务处理
                tmp = file_context[tmpStart:tmpIndex]
                tasklist.append(tmp)
        return tmpIndex

    def _DealTaskList(self):
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
        if startKey == "" and endKey == "":
            logging.error("GetVar 不允许左右key都为空")
            return {"0": "", "1": -1}
        tmpStart =0
        if(startKey != ""):
            tmpStart = str.find(startKey, index)
            while tmpStart != -1 and self.CheckIsStr(str,tmpStart):
                tmpStart = str.find(startKey, tmpStart+len(startKey))
        tmpEnd = -1
        if endKey != "":
            tmpEnd = str.find(endKey, tmpStart + len(startKey))
            while tmpEnd != -1 and self.CheckIsStr(str, tmpEnd):
                tmpEnd = str.find(endKey, tmpEnd + len(startKey))
        if (tmpStart == -1 or (endKey != "" and tmpEnd == -1)):
            #logging.error("GetVar 获取变量失败，startKey[%s],endKey[%s],index[%s]\nstr[%s]"%(startKey,endKey,index,str[index:]))
            return {"0": "", "1": -1}

        if tmpEnd != -1:
            tmp = self.FormatData(str[tmpStart + len(startKey):tmpEnd])
        else:
            tmp = self.FormatData(str[tmpStart + len(startKey):])
        return {"0":tmp,"1":tmpEnd}

    def FormatData(self,str):
        retVal = str.strip()
        if retVal[0] == self.strltab and retVal[-1] == self.strrtab:#如果有字符串符，就去掉
            retVal= retVal[1:-1].strip()
        return retVal

    def GetVarList(self,str):
        RetMap = []
        tmpMap = self.GetVar(str, "", self.tab, 0)
        tmpMap["1"] != -1
        while tmpMap["1"] != -1:
            RetMap.append(tmpMap["0"])
            tmpMap = self.GetVar(str, self.tab, self.tab, tmpMap["1"])
        if tmpMap["1"] == -1:
            tmpMap["1"] = 0
        tmpMap = self.GetVar(str, self.tab, "", tmpMap["1"])
        if tmpMap["0"] != "":
            RetMap.append(tmpMap["0"])
        return RetMap

    def sleep(self,str):
        logging.error("sleep %s"%str)
        time.sleep(int(str))

    def CheckIsStr(self,str,index):
        i = 0
        for num in range(0,index):
            if str[num] == self.strltab:
                i = i+1
            elif str[num] == self.strrtab:
                i = i-1
            if i < 0:
                logging.error("CheckIsStr 校验是否是字符串，左括号和右括号不对称，str[%s],index[%s]" % (str, index))
                return False
        return i > 0
