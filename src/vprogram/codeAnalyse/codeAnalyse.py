import  logging
from mydatabase import *
from mycomm import *

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
        return self.PyMergeStr(Array)
    #过滤文件名
    def PyfilterFile(self,str):
        return str.endswith(".py")
    #处理代码每行的数据
    def PyDealArrayData(self,Arraydata):
        mindata = []
        minfunc = ""
        minclass = ""
        oldStr = None
        tabnum = self.PyGetTabNum(Arraydata[0])
        for data in Arraydata:
            if oldStr is not None:
                self.PyDealArrayDataIn(mindata, minfunc, minclass)
                mindata.clear()
                oldStr = None

            tabnumTmp = self.PyGetTabNum(data)  # 获取子范围内的数据
            if (tabnumTmp > tabnum):
                mindata.append(data)

            if tabnumTmp == tabnum:
                if (len(mindata) > 0):
                    oldStr = data
                self.PyGetInfo(data)
        if (len(mindata) > 0):
            self.PyDealArrayDataIn(mindata, minfunc, minclass)

        return
    #递归处理每行的数据
    def PyDealArrayDataIn(self, Arraydata, func, classname):
        mindata = []
        minfunc = func
        minclass = classname
        oldStr = None
        tabnum = self.PyGetTabNum(Arraydata[0])
        for data in Arraydata:
            if oldStr is not None:
                self.PyDealArrayDataIn(mindata,minfunc,minclass)
                mindata.clear()
                oldStr = None

            tabnumTmp = self.PyGetTabNum(data)#获取子范围内的数据
            if(tabnumTmp > tabnum):
                mindata.append(data)

            if tabnumTmp == tabnum:
                if (len(mindata) > 0):
                    oldStr = data
                self.PyGetInfo(data)
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
    def PyGetParam(self,data):
        flag = 0
        data = self.delNotes(data)
        for char in data:
            continue
        return flag
    #获取函数
    def PyGetFunc(self,data):
        data = self.delNotes(data)
        return 0
    #获取类
    def PyGetClass(self,data):
        data = self.delNotes(data)
        return 0
    #获取信息
    def PyGetInfo(self,data):
        if self.PyGetParam(data) >0:
            return 1
        if self.PyGetFunc(data) >0:
            return 2
        if self.PyGetClass(data) >0:
            return 3
        return 0
    #删除行注释
    def delNotes(self,str):
        len1 = len(str)
        while len1 >= 0:
            len1 -= 1
            if str[len1] == "#":
                break
        pass
    #合并数组 合并\换行以及 ''' 和"""的字符串数组
    def PyMergeStr(self,Array):
        tmpArray = []
        num = 0
        newnum = 0
        StrChar = ""
        tmp = ""
        flag = False
        appendFlag = True
        for data in Array:
            #如果是\最后的话，不管是不是字符串都合并
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
                tmpArray.append(tmp + data)
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
        if char != '"' || char != "'":
            return flag[0]

        if flag[2] == 0:
            if char == "'" or char == '"': #置初始
                flag[0] = 1
                flag[1] = char
                flag[2] = 1
                flag[3] = 0
                return flag[0]
        else if flag[2] == 1 or flag[2] == 3: #1或3都有可能识别成字符串
            if char != flag[1]: #不是识别符，则清结束数量
                flag[3] = 0
                return flag[0]
            if flag[2] == 1：
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
        else if flag[2] == 2: #
            if char != flag[1]: #重置
                flag[0] = 0
                flag[1] = ''
                flag[2] = 0
                flag[3] = 0
                return flag[0]
            flag[0] = 1
            flag[2] = 3
            return flag[0]
            
