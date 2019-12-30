import  logging, re
from mydatabase import *
from mycomm import *

class CommCodeData():
    def __init__(self,line,Data):
        self.line = str(line)
        self.data = Data
        self.func = ""
        self.classname = ""

class CommCodeDataMap():
    def __init__(self,ArrayData):
        self.list = []
        i = 0 
        for Data in ArrayData:
            i += 1
            CommCodeData1 = CommCodeData(i,Data)
            self.list.append(CommCodeData1)
    
    def append(self,CommCodeData1:CommCodeData):
        self.list.append(CommCodeData1)

    def __len__(self):
        return len(self.list)

    def clear(self):
        self.list.clear()

class commCode(mydatabase_table):
    table_infos = {"code_var":{"table_name":"code_var",
                                "desc":"描述代码的变量",
                                "table_col":    [{"col":"name", "opt": " VARCHAR(64)"},
                                                {"col": "type", "opt": " VARCHAR(64)"},
                                                {"col":"istatic","opt":" NUMBER"},
                                                {"col": "subsclass", "opt": "VARCHAR(64) "},
                                                {"col": "declare_file", "opt": "VARCHAR(512)"},
                                                {"col": "declare_line", "opt": "VARCHAR(32)"},
                                                {"col": "real_file", "opt": "VARCHAR(512)"},
                                                {"col": "real_line", "opt": "VARCHAR(32)"},
                                                {"col":"DESC","opt":" VARCHAR(128)"}
                                                ]},
                   "code_function": {"table_name": "code_function",
                                "desc": "描述代码的函数",
                                "table_col": [{"col": "name", "opt": " VARCHAR(64)"},
                                              {"col": "type", "opt": " VARCHAR(64)"},
                                              {"col": "istatic", "opt": " NUMBER"},
                                              {"col": "return_type", "opt": " VARCHAR(64)"},
                                              {"col": "subsclass", "opt": "VARCHAR(64) "},
                                              {"col": "declare_file", "opt": "VARCHAR(512)"},
                                              {"col": "declare_line", "opt": "VARCHAR(32)"},
                                              {"col": "real_file", "opt": "VARCHAR(512)"},
                                              {"col": "real_line", "opt": "VARCHAR(32)"},
                                              {"col": "DESC", "opt": " VARCHAR(256)"}
                                              ]},
                   "code_param": {"table_name": "code_param",
                                     "desc": "描述代码的函数",
                                     "table_col": [{"col": "name", "opt": " VARCHAR(64)"},
                                                   {"col": "type", "opt": " VARCHAR(64)"},
                                                   {"col": "istatic", "opt": " NUMBER"},
                                                   {"col": "subsclass", "opt": "VARCHAR(64) "},
                                                   {"col": "declare_file", "opt": "VARCHAR(512)"},
                                                   {"col": "declare_line", "opt": "VARCHAR(32)"},
                                                   {"col": "real_file", "opt": "VARCHAR(512)"},
                                                   {"col": "real_line", "opt": "VARCHAR(32)"},
                                                   {"col": "DESC", "opt": " VARCHAR(128)"}
                                                   ]},
                   }
    def __init__(self,cursor):
        super().__init__(cursor)

    tab = " "
    #读取py文件信息
    def LoadFromPy(self,projectdir):
        filelist = []
        dir_list = []
        get_file_path(projectdir,filelist,dir_list)
        for file in filelist:
            if True != self.PyfilterFile(file):
                continue
            with open(file, 'rb') as fp:
                code_data=fp.read()
            code_data = str(code_data,encoding = "utf8")
            Arraydata = self.PysplitLine(code_data)
            self.PyDealArrayData(Arraydata)
    #将整个代码文件分行合并
    def PysplitLine(self,str):
        str = str.replace("\r","")
        str = str.replace("\t", " ")
        Array = str.split("\n")
        #统计行号
        CommCodeDataMap1 = CommCodeDataMap(Array)
        return self.PyMergeStr(CommCodeDataMap1)
    #过滤文件名
    def PyfilterFile(self,str):
        return str.endswith(".py")
    #处理代码每行的数据
    def PyDealArrayData(self,Arraydata:CommCodeDataMap):
        mindata = CommCodeDataMap([])
        minfunc = ""
        minclass = ""
        tabnum = self.PyGetTabNum(Arraydata.list[0].data)
        for Mapdata in Arraydata.list:
            tabnumTmp = self.PyGetTabNum(Mapdata.data)  # 获取子范围内的数据
            if (tabnumTmp > tabnum):
                mindata.append(Mapdata)

            if tabnumTmp == tabnum:
                if (len(mindata) > 0):
                    self.PyDealArrayDataIn(mindata, minfunc, minclass)
                    mindata.clear()
                self.PyGetInfo(Mapdata)
        if (len(mindata) > 0):
            self.PyDealArrayDataIn(mindata, minfunc, minclass)

        return
    #递归处理每行的数据
    def PyDealArrayDataIn(self, Arraydata:CommCodeDataMap, func, classname):
        mindata = CommCodeDataMap([])
        minfunc = func
        minclass = classname
        tabnum = self.PyGetTabNum(Arraydata.list[0].data)

        for Mapdata in Arraydata.list:
            tabnumTmp = self.PyGetTabNum(Mapdata.data)#获取子范围内的数据
            if(tabnumTmp > tabnum):
                mindata.append(Mapdata)

            if tabnumTmp == tabnum:
                if (len(mindata) > 0):
                    self.PyDealArrayDataIn(mindata,minfunc,minclass)
                    mindata.clear()
                self.PyGetInfo(Mapdata)
        if(len(mindata)>0):
            self.PyDealArrayDataIn(mindata, minfunc, minclass)
        pass

    #获取代码前置数
    def PyGetTabNum(self,data):
        ret = 0
        for char in data:
            if char == " ":
                ret += 1
                continue
            break
        return ret
    #获取变量和变量定义
    def PyGetParam(self,Mapdata:CommCodeData):
        flag = 0
        value = self.GetKeyLeftAndRight(Mapdata.data,'=')
        if len(value) == 0:
            return flag
        
        return flag
    #获取函数
    def PyGetFunc(self,data:CommCodeData):
        return 0
    #获取类
    def PyGetClass(self,data:CommCodeData):
        return 0

    def reverse(self,str):
        return str[::-1]

    def checkInNormalstr(self,char):
        ret = re.match("[a-zA-Z0-9_]",char)
        if ret == None :
            return False
        return True
        
    def GetKeyLeftAndRight(self,str,keychar):
        flag=[0,'',0,0]
        len1 = len(str)
        i = 0
        leftValue = ""
        while(i < len1):
            if 0 == self.PyCheckIsStr(str[i],flag) :
                if str[i] != keychar:
                    if self.checkInNormalstr(str[i]):
                        leftValue += str[i]
                    else:
                        leftValue = "" #清掉
                    
                elif str[i] == keychar:
                    #去掉如==之类的情况
                    if(i+1<len1 and str[i+1] != keychar):
                        rightValue = str[i+1].lstrip()
                        i=0
                        len1=len(rightValue)
                        while (i < len1):
                            if False == self.checkInNormalstr(str[i]):
                                rightValue = rightValue[0:i]
                                break
                        return [leftValue,rightValue]
                    
                    while(i+1<len1 and str[i+1] == keychar):
                        i+=1
                        self.PyCheckIsStr(str[i],flag) #为了保证字符串判定正常
                
            i+=1
        return []

        
        
    #获取信息
    def PyGetInfo(self,Mapdata:CommCodeData):
        logging.debug('PyGetInfo [%s]%s'%(Mapdata.line,Mapdata.data))
        Mapdata.data = self.delNotes(Mapdata.data)
        retval =0;
        if self.PyGetParam(Mapdata) >0:
            retval +=1
        if self.PyGetFunc(Mapdata) >0:
            retval +=2
        if self.PyGetClass(Mapdata) >0:
            retval +=4
        return retval
    
    #删除行注释
    def delNotes(self,str):
        flag=[0,'',0,0]
        len1 = len(str)
        i = 0
        while(i < len1):
            if(0 == self.PyCheckIsStr(str[i],flag) and str[i] == '#'):#后续都是注释干掉
                return str[0:i]
            i+=1
        return str

    #合并数组 合并\换行以及 ''' 和"""的字符串数组
    def PyMergeStr(self,Array:CommCodeDataMap):
        tmpArray = CommCodeDataMap([])
        num = 0
        newnum = 0
        StrChar = ""
        tmp = ""
        flag = False
        appendFlag = True
        lineStart = ""
        for Mapdata in Array.list:
            #如果是\最后的话，不管是不是字符串都合并
            data = Mapdata.data
            if lineStart == "":
                lineStart = Mapdata.line
            dataArr=data.split("\\")
            if len(dataArr) >1 and len(dataArr[-1].replace(" ","")) == 0:
                tmp += data + "\n"
                continue
            #如果是字符串的话
            for char in data:
                if StrChar == "'" or StrChar == '"':
                    if char == StrChar:
                        if flag == True:
                            newnum += 1
                            if newnum == num:
                                num = 0
                                newnum = 0
                                flag = False
                                StrChar = ""
                                appendFlag = True
                                break
                        else:
                            if num < 2:
                                num += 1
                            else:
                                num = 3
                                flag = True
                                appendFlag = False
                    else:
                        if num == 2:
                            StrChar = ""
                            num = 0
                        elif flag == False:
                            flag = True
                else:
                    if char == "'" or char == '"':
                        StrChar = char
                        num = 1

            if appendFlag == True:
                CommCodeData1 = CommCodeData(lineStart + "_" + Mapdata.line,tmp + data)
                tmpArray.append(CommCodeData1)
                lineStart = ""
                tmp = ""
            else:
                tmp += data + "\n"
        return tmpArray

    #检查是否在str范围 flag最初为=[0,'',0,0],使用时得PyCheckIsStr(char,flag) ,返回值不为0则为字符串
    '''
        flag[0] 表示是否是字符串范围 0非字符串 1待比对字符串开始标识 
        flag[1] 保存字符串的比对标识
        flag[2] 保存字符串比对标识的开始数量
        flag[3] 保存字符串比对标识的结束数量
    '''
    def PyCheckIsStr(self,char,flag:[]):
        if char != '"' or char != "'":
            return flag[0]

        if flag[2] == 0:
            if char == "'" or char == '"': #置初始
                flag[0] = 1
                flag[1] = char
                flag[2] = 1
                flag[3] = 0
                return flag[0]
        elif flag[2] == 1 or flag[2] == 3: #1或3都有可能识别成字符串
            if char != flag[1]: #不是识别符，则清结束数量
                flag[3] = 0
                return flag[0]
            if flag[2] == 1:
                flag[0] = 0
                flag[2] = 2
                return flag[0]
            flag[3]+=1
            if flag[3] == 3:
                flag[0] = 0
                flag[1] = ''
                flag[2] = 0
                flag[3] = 0
            return 1 #即使最后一个字符串标识符也是按1返回
        elif flag[2] == 2: #
            if char != flag[1]: #重置
                flag[0] = 0
                flag[1] = ''
                flag[2] = 0
                flag[3] = 0
                return flag[0]
            flag[0] = 1
            flag[2] = 3
            return flag[0]
            
