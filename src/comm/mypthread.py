# coding=utf-8
import threading,logging
from contextlib import contextmanager
from globalConfig import *

@contextmanager
def call():
    #logging.debug("opcode:%s,lThreadPool:%s begin" % (str(lThreadPool.opcode), str(lThreadPool)))
    yield
    #logging.debug("opcode:%s,lThreadPool:%s end" % (str(lThreadPool.opcode), str(lThreadPool)))



class mypthread(threading.Thread):
    def __init__(self, func, arg,opcode):
        super(mypthread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.arg = arg
        self.func = func
        self.opcode = opcode

    def run(self):  # 定义每个线程要运行的函数
        lThreadPool.opcode = self.opcode
        with call():
            self.func(self.arg)


