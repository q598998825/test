import logging,os,traceback

from vscript_rule import *
from vscript_dm import *
from myCommDM import *



class vscript:
    def __init__(self):
        comm_param1 = comm_param()
        vscript_list1 = vscript_list()
        self.vscriptPath = comm_param1.GetResult(comm_param1.useDefaultSql("getValue","VSCRIPT_PATH"))[0]["VALUE"]
        self.vscriptList = comm_param1.GetResult(vscript_list1.useDefaultSql("getList"))
        pass

    def run(self):
        vpro_rule1 = vpro_rule()
        for tmpvscript in self.vscriptList:
            tmpPath = self.vscriptPath + "/" + tmpvscript["FILENAME"]
            tmpPath = os.path.abspath(tmpPath)

            file = open(tmpPath, 'r', encoding='utf-8')
            try:
                file_context = file.read() #读取文件
                vpro_rule1.exec(tmpvscript,file_context)
            except Exception as e:
                logging.error("vscript 执行任务异常 [%s]：%s \n%s" % (tmpvscript["NAME"], e.__str__(), traceback.format_exc()))
            finally:
                file.close()
