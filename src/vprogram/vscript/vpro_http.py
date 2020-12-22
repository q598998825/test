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

    def http(self,toml_data):
        # 获取参数
        ip = toml_data["servIp"]
        if ip == "":
            logging.error("http 无法获取服务ip")
            exit(-1)

        port = toml_data["servPort"]
        if port == "":
            logging.error("http 无法获取 port")
            exit(-1)

        self.httpInit(ip,port)

        return 0

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

    def post(self,config,key,value):
        logging.debug("post func begin")
        tasklist = []
        value=self._taskExec(value,tasklist)

        url = config["url"]
        httpHead = config["heads"]
        httpBody = value
        logging.debug("post %s \r\n%s\r\n\r\n%s"%(url,httpHead,httpBody))
        #获取报文头
        if httpHead != "":
            headers = json.loads(httpHead)
            r=requests.post(url, data=httpBody.encode('utf8'), headers=headers)
        else:
            r=requests.post(url, data=httpBody)
        logging.debug(r.text)
        logging.debug("post func end")
