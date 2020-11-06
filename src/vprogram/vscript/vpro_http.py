# coding=utf-8
import logging,requests,json
import os
from globalConfig import *
from mypthread import *
import sys

class vpro_http:
    def __init__(self):#子类统一初始化
        self.HttpServerKey = "HttpServer"
        pass

    def http(self,str):
        # 获取参数
        tmpMap = self.httpGetVar(str)

        self.httpInit(tmpMap[0],tmpMap[1])

        # 获取任务列表
        tasklist = []
        tmpstr = tmpMap[2]
        self._GetTaskList(tasklist, tmpstr)

        #处理程序
        self.taskExec(tasklist)

        return 0


    def httpGetVar(self,str):
        tmpMap = self.GetVarList(str)
        ip = tmpMap[0]
        if ip == "":
            logging.error("http 无法获取服务ip")
            exit(-1)

        port = tmpMap[1]
        if port == "":
            logging.error("http 无法获取 port")
            exit(-1)

        return tmpMap

    def httpInit(self,ip,port):
        data = {"ip":ip,"port":port}
        opcode = lThreadPool.opcode + "_httpServer"
        mypthread1 = mypthread(self.httpProc, data, opcode)
        mypthread1.start()

    def httpProc(self,arg):

        argv = []
        argv.append("manage.py")
        argv.append("runserver")
        argv.append("%s:%s" % (arg["ip"], arg["port"]))
        argv.append("--noreload")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'httpServer.settings')
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(argv)

    def post(self,str):
        logging.debug("post func begin")
        tmpMap = self.GetVarList(str)
        if len(tmpMap) <3:
            logging.error("post 入参不正常")
            return
        url = tmpMap[0]
        httpHead = tmpMap[1]
        httpBody = tmpMap[2]
        logging.debug("post %s \r\n%s\r\n\r\n%s"%(url,httpHead,httpBody))
        #获取报文头
        if httpHead != "":
            headers = json.loads(httpHead)
            r=requests.post(url, data=httpBody.encode('utf8'), headers=headers)
        else:
            r=requests.post(url, data=httpBody)
        logging.debug(r.text)
        logging.debug("post func end")
