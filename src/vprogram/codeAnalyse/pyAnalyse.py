import  logging, re

class pyAnalyseData():
    def __init__(self,data,line):
        self.data = data
        self.line = line

class pyAnalyse():
    def __init__(self):
        self.ArrayData=[]
        self.charflag= [0,'',0,0]
        self.charflag_flag = 0
        self.charflag_char = 1
        self.charflag_startNum = 2
        self.charflag_endNum = 3
        pass
    def LoadFromFile(self,FilePath):
        with open(file, 'rb') as fp:
            code_data=fp.read()
        self.splitData(code_data)


    def splitData(self,code_data):
        linenum = 1
        oneData = ""
        for char in code_data:                
            if char == "\n":
                self.ArrayData.append(pyAnalyseData(oneData,linenum))
                linenum += 1
                continue
            elif char == "\t"
                continue
            elif 

    def isSplitChar(self,char):
        ret = re.match("[ \{\}\[\],]",char)
        if ret == None :
            return False
        return True


    '''
        flag[0] 表示是否是字符串范围 0非字符串 1标识为字符串 
        flag[1] 保存字符串的比对标识
        flag[2] 保存字符串比对标识的开始数量
        flag[3] 保存字符串比对标识的结束数量
    '''
    def PyCheckIsStr(self,char):
        if char != '"' or char != "'":
            return self.charflag[self.charflag_flag]

        if self.charflag[self.charflag_startNum] == 0:
            if char == "'" or char == '"': #置初始
                self.charflag = [1,char,1,0]
                return self.charflag[self.charflag_flag]

        elif self.charflag[self.charflag_startNum] == 1 or self.charflag[self.charflag_startNum] == 3: #1或3都有可能识别成字符串
            if char != self.charflag[self.charflag_char]: #不是识别符，则清结束数量
                self.charflag[self.charflag_endNum] = 0
                return self.charflag[self.charflag_flag]
            if self.charflag[self.charflag_startNum] == 1:
                self.charflag[self.charflag_flag] = 1
                self.charflag[self.charflag_startNum] = 2
                return self.charflag[self.charflag_flag]
            self.charflag[self.charflag_endNum]+=1
            if self.charflag[self.charflag_endNum] == 3:
                self.charflag = [0,'',0,0]
            return 1 #即使最后一个字符串标识符也是按1返回

        elif self.charflag[self.charflag_startNum] == 2: #
            if char != self.charflag[1]: #重置
                self.charflag = [0,'',0,0]
                return self.charflag[self.charflag_flag]
            self.charflag[self.charflag_startNum] = 3
            return self.charflag[self.charflag_flag]
        
        #这边都是异常
        raise("PyCheckIsStr 函数异常")
