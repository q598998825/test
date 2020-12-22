# coding=utf-8
import logging,socket,time,re
from wsgiref.simple_server import make_server
from myCommDM import *
from vscript_dm import *
from vpro_socket import *
from vpro_http import *

class vpro_rule(vpro_socket,vpro_http):
    def __init__(self):
        self.startKey = '<12 '
        self.endKey = ' 21>'
        self.tab = ','
        self.strltab = '{'
        self.strrtab = '}'
        self.ruleMap={""}
        self.Data={}
        #子类初始化
        vpro_socket.__init__(self)
        vpro_http.__init__(self)

    def exec(self,tmpvscript,toml_data):
        #初始化数据
        self.InitData(tmpvscript,toml_data)
        
        #处理任务
        self._DealTaskList(self.toml_data)

    # ********************************************** 下面为标准一般不动的函数 ******************************

    def _InitConfig(self,toml_data):
        if "config" not in toml_data:
            return
        config = toml_data["config"]
        ret = None
        if "needServ" in config and config["needServ"] :
            ret = eval("self." + config["type"])(toml_data["config"])
        return ret

    def InitData(self,tmpvscript,toml_data):
        self.vscript = tmpvscript
        self.toml_data = toml_data
        self.tasklist = {}

    def _taskExec(self,str,tasklist=[]):
        index = 0
        tmpArray = []
        tasklist1=[]
        while index != -1:
            index = self._GetTaskList_in(str,tasklist1,tmpArray,index)

        #格式化
        for tmpTask in tasklist1:
            tmpMap = self.GetVar(tmpTask, self.startKey, self.tab, 0)
            funcname = tmpMap["0"]
            if (funcname == ""):
                logging.error("taskExec has not rule Func")
                exit
            endindex = tmpMap["1"]
            # 获取规则处理对象
            tmpstr = self.FormatData(tmpTask[endindex + 1:-len(self.endKey)])
            # 处理
            ret = eval("self." + funcname)(tmpstr)
            str = str.replace(tmpTask,ret)
        return str


    def _GetTaskList_in(self,str,tasklist=[],tmpArray=[],index=0):
        startIndex = str.find(self.startKey,index)
        endIndex = str.find(self.endKey,index)
        if startIndex != -1 and \
            startIndex < endIndex:
            #当先找到开始key,且开始key比结束key还前则加进去
            tmpArray.append(startIndex)
            ret=self._GetTaskList_in(str,tasklist,tmpArray,startIndex+1)
            return ret
        elif endIndex != -1 and \
                (endIndex < startIndex or startIndex == -1):
            #当找到结束符就用结束符的内容
            tmp = tmpArray.pop()
            tmpStr = str[tmp:endIndex+len(self.endKey)]
            tasklist.append(tmpStr)
            return endIndex+len(self.endKey)
        return -1


    def _DealTaskList_in(self,toml_data):
        # 获取规则函数名
        ret = 0
        if "config" not in toml_data:
            logging.error("_DealTaskList_in 没有 config")
            return
        config = toml_data["config"]
        funcname = config["type"]
        # 获取规则处理对象
        for task in toml_data:
            if task == "config":
                continue
            ret = eval("self." + funcname)(config,task,toml_data[task])

        return ret

    def _DealTaskList(self,toml_data):

        self._InitConfig(toml_data)

        for task in toml_data:
            logging.debug("执行任务 task[%s]" % task)
            if task.find("func") != -1:
                self._DealTaskList_in(toml_data[task])

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
            tmp = self.FormatData(str[tmpStart + len(startKey):tmpEnd],False)
        else:
            tmp = self.FormatData(str[tmpStart + len(startKey):],False)
        return {"0":tmp,"1":tmpEnd}

    def FormatData_in(self,str,map,index):
        retval = str
        tmpStart =0
        tmpindex = index
        while tmpStart != -1:
            tmpStart = retval.find(self.startKey, tmpindex)
            tmpEnd = retval.find(self.endKey, tmpindex)
            if tmpStart != -1 and tmpStart < tmpEnd:
                map.append(tmpStart)
                #递归，因为待处理的字符串被替换，所以重新计算
                retval = self.FormatData_in(retval,map,tmpStart+len(self.startKey))
                tmpindex = index

            elif tmpEnd != -1 and \
                 (tmpEnd < tmpStart or tmpStart == -1):
                tmpStart = map.pop()
                tmpEnd = tmpEnd+len(self.endKey)
                tmp = self._DealTaskList_in(retval[tmpStart:tmpEnd])
                tmp1 = retval[tmpEnd]
                if retval[tmpStart-1] == self.strltab and \
                    retval[tmpEnd] == self.strrtab:
                    retval = retval[0:tmpStart-1] + tmp + retval[tmpEnd+1:]
                else:
                    retval = retval[0:tmpStart] + tmp + retval[tmpEnd:]
                tmpindex = tmpStart +len(tmp)

        #else:
            #pass
        return retval

    def FormatData(self,str,do_func = True):
        retVal = str.strip()
        if retVal[0] == self.strltab and retVal[-1] == self.strrtab:#如果有字符串符，就去掉
            retVal= retVal[1:-1].strip()
            #如果有 startKey 或者 endKey则继续执行
        if do_func:
            map = []
            index = 0
            retVal = self.FormatData_in(retVal,map,index)
        return retVal

    def GetVarList(self,str):
        RetMap = []
        tmpMap = self.GetVar(str, "", self.tab, 0)
        oldIndex = 0
        tmpMap["1"] != -1
        while tmpMap["1"] != -1:
            oldIndex = tmpMap["1"]
            RetMap.append(tmpMap["0"])
            tmpMap = self.GetVar(str, self.tab, self.tab, tmpMap["1"])
        if tmpMap["1"] == -1:
            tmpMap["1"] = oldIndex
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

    def getData(self,str):
        str = str.replace("\r","")
        str = str.replace("\n", "")
        if str.find("sqlStr_") == 0 or \
                str.find("sqlVau_") == 0:
            comm_param1 = comm_param()
            vscript_list1 = vscript_list()
            return comm_param1.GetResult(vscript_list1.useDefaultSql("getData", str[7:]))[0]["VALUE"]
        else:
            return self.Data[str]

    def setData(self,config,taskid,taskvalue):
        return self._SetData(config,taskid,taskvalue)

    def _SetData(self,config,key,value):
        if "substype" in config\
                and -1 != config["substype"].find("sql"):
            #插入数据库
            if config["substype"]== "sqlVau":
                value = "'"+value+"'"
            vscript_list1 = vscript_list()
            vscript_list1.useDefaultSql("setData",key,value)
            comm_param1 = comm_param()
            comm_param1.commit()
        else:
            #插入变量名
            self.Data[key] = value
        return True

    def taskExec(self,tasklist,do_func = True):
        for str in tasklist:
            # 获取规则函数名
            tmpMap = self.GetVar(str, self.startKey, self.tab, 0)
            funcname = tmpMap["0"]
            if (funcname == ""):
                logging.error("taskExec has not rule Func")
                exit
            endindex = tmpMap["1"]
            # 获取规则处理对象
            tmpstr = self.FormatData(str[endindex + 1:-len(self.endKey)],do_func)
            # 处理
            ret = eval("self." + funcname)(tmpstr)
