# coding=utf-8
import logging,os,traceback,copy,toml

from vscript_rule import *
from vscript_dm import *
from myCommDM import *
from mypthread import *


class vscript:
    def __init__(self):
        comm_param1 = comm_param()
        vscript_list1 = vscript_list()
        self.vscriptPath = comm_param1.GetResult(comm_param1.useDefaultSql("getValue","VSCRIPT_PATH"))[0]["VALUE"]
        self.vscriptList = comm_param1.GetResult(vscript_list1.useDefaultSql("getList"))
        pass

    def run(self):
        for tmpvscript in self.vscriptList:
            Data = {}
            Data["data"] = tmpvscript
            Data["opcode"]="vscript_%s"%tmpvscript["NAME"]
            mypthread1 = mypthread(self.Proc, Data,Data["opcode"])
            mypthread1.start()

    def Proc(self,arg):
        tmpvscript = arg["data"]
        lThreadPool.mydatabase1 = mydatabase()
        vpro_rule1 = vpro_rule()
        tmpPath = self.vscriptPath + "/" + tmpvscript["FILENAME"]
        tmpPath = os.path.abspath(tmpPath)

        tomldata = toml.load(tmpPath)
        try:
            #file_context = file.read()  # 读取文件
            vpro_rule1.exec(tmpvscript, tomldata)
        except Exception as e:
            logging.error("vscript 执行任务异常 [%s]：%s \n%s" % (tmpvscript["NAME"], e.__str__(), traceback.format_exc()))
        finally:
            lThreadPool.mydatabase1.commit()
