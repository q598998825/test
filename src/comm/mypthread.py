# coding=utf-8
import threading

class mypthread(threading.Thread):
    def __init__(self, func, arg):
        super(mypthread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.arg = arg
        self.func = func

    def run(self):  # 定义每个线程要运行的函数
        self.func(self.arg)
