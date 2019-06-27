# coding=utf-8
from mysingleton import *
from mypthread import *
import threading
from mymsg import *

def myTimerMngInit():
    myTimerMng1 = myTimerMng()
    return 0

def myTimerMngProc(msg):
    pass

@singleton
class myTimerMng():
    def __init__(self):
        self.timer = None


    def SendTimerMsgFunc(self,arg):
        MyMsgPkg1 = MyMsgPkg()
        MyMsgPkg1.From = "Timer"

        sendMsgself(MyMsgPkg1)

