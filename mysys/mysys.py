# coding=utf-8
import os, sys,importlib,logging,threading,traceback
import json
from src.comm.mysingleton import *
from src.comm.mypthread import *
from src.comm.mydatabase import *

mySysMustInit = [{"name": "mysysin","file": "mysysin","notes": "统一初始化"}]

class funcData():
    def __init__(self):
        self.pcode = None
        self.Proc = None
        self.msg = []
        self.sem = threading.Semaphore()

    def addmsg(self,data):
        self.msg.append(data)

    def getmsg(self):
        self.lock()
        if len(self.msg) == 0 :
            return None
        return self.msg.pop()
    def lock(self):
        self.sem.acquire()
    def unlock(self):
        self.sem.release()

@singleton
class mysys():
    file_list = []
    dir_list = []
    FuncList = {}
    vprogramPath = os.path.abspath("./mysysdir/config/vprogram.json")
    def __init__(self):
        pass

    def get_file_path(self,path, file_list, dir_list):
        dir_list.append(path)
        self.get_file_path_in(path, file_list, dir_list)

    def get_file_path_in(self,path, file_list, dir_list):
        # 获取该目录下所有的文件名称和目录名称
        dir_or_files = os.listdir(path)
        for dir_file in dir_or_files:
            # 获取目录或者文件的路径
            dir_file_path = os.path.join(path, dir_file)
            # 判断该路径为文件还是路径
            if os.path.isdir(dir_file_path):
                dir_list.append(dir_file_path)
                # 递归获取所有文件和目录的路径
                self.get_file_path_in(dir_file_path, file_list, dir_list)
            else:
                file_list.append(dir_file_path)

    def InitEnv(self):
        root_path = os.path.abspath(".")
        self.get_file_path(root_path,self.file_list,self.dir_list)
        logging.debug(self.file_list)
        self.InitEnvDir()
        self.InitEnvPy()

    def InitEnvDir(self):
        for dir in self.dir_list:
            sys.path.append(dir)

    def InitEnvPy(self):
        #初始化必要进程
        for vprogram in mySysMustInit:
            #导入文件
            try:
                program = importlib.import_module(vprogram['file'])
                program.Init(self)
            except Exception as e:
                logging.error("导入python子系统异常[%s]：%s\n%s"%(vprogram['name'],e.__str__(),traceback.format_exc()))
                os._exit(1)

        lThreadPool.opcode = "mysys"
        lThreadPool.mydatabase1 = mydatabase()

        #初始化配置文件进程
        file = open(self.vprogramPath, 'r', encoding='utf-8')
        vprogram_list = json.load(file)
        for vprogram in vprogram_list:
            #导入文件
            try:
                program = importlib.import_module(vprogram['file'])
                if(0 > program.Init()):
                    logging.error("导入python子系统异常[%s]" % (vprogram['name']))
                    os._exit(1)
                self.addProcess(vprogram['name'],program)
                lThreadPool.mydatabase1.commit()
            except Exception as e:
                logging.error("导入python子系统异常[%s]：%s \n%s"%(vprogram['name'],e.__str__(),traceback.format_exc()))
                lThreadPool.mydatabase1.rollback()
                os._exit(1)

    def InitEnvProc(self,arg):
        funcData1 = arg
        if funcData1 is not None: #初始化
            lThreadPool.opcode = funcData1.opcode
            lThreadPool.mydatabase1 = mydatabase()

        while True:
            #处理进程
            data = funcData1.getmsg()
            if data is None:
                continue
            try:
                funcData1.Proc(data)
                lThreadPool.mydatabase1.commit()
            except Exception as e:
                logging.error("执行opcode异常[%s]：%s \n%s" % (funcData1.opcode, e.__str__(), traceback.format_exc()))
                lThreadPool.mydatabase1.rollback()

    def addProcess(self,opcode,program):
        if(opcode in self.FuncList):
            return None
        self.FuncList[opcode] = funcData()
        self.FuncList[opcode].opcode = opcode
        self.FuncList[opcode].Proc = program.Proc
        mypthread1 = mypthread(self.InitEnvProc, self.FuncList[opcode])
        mypthread1.start()
        return self.FuncList[opcode]

    def addProc(self,opcode,proc):
        if(opcode in self.FuncList):
            return None
        self.FuncList[opcode] = funcData()
        self.FuncList[opcode].opcode = opcode
        self.FuncList[opcode].Proc = proc
        mypthread1 = mypthread(self.InitEnvProc, self.FuncList[opcode])
        mypthread1.start()
        return self.FuncList[opcode]

    def sendmsg(self,MsgPkg):
        if MsgPkg is None or MsgPkg.To is None:
            logging.error("msg[%s] has not [To] info" % (str(MsgPkg)))
            return
        if MsgPkg.Data is None:
            logging.error("msg[%s] has not [Data] info" % (str(MsgPkg)))
            return
        if MsgPkg.To not in self.FuncList:
            logging.error("msg.To[%s] not in Funclist" % (str(MsgPkg.To)))
            return
        self.FuncList[MsgPkg.To].addmsg(MsgPkg)
        self.FuncList[MsgPkg.To].unlock()
