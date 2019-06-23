# coding=utf-8
import os, sys,importlib,logging
import json
from src.comm.mycomm import *
from src.comm.mypthread import *

mySysMustInit = [{"name": "mysysin","file": "mysysin","notes": "统一初始化"}]

class funcData():
    opcode = None
    Proc = None

class mysys():
    file_list = []
    dir_list = []
    FuncList = {}
    vprogramPath = os.path.abspath("./mysys/config/vprogram.json")
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
                logging.error("导入python子系统异常[%s]：%s"%(vprogram['name'],e.__str__()))
                os._exit(1)

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
            except Exception as e:
                logging.error("导入python子系统异常[%s]：%s"%(vprogram['name'],e.__str__()))
                os._exit(1)

    def InitEnvProc(self,arg):
        funcData1 = arg
        funcData1.Proc("123")

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