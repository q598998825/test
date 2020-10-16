# coding=utf-8
from mysingleton import *
import threading,logging,time
from mymsg import *
from mycomm import *

def myTimerMngInit():
    myTimerMng1 = myTimerMng()
    return 0

def myTimerMngProc(msg):
    pass

@singleton
class myTimerMng():
    pool = []

    def __init__(self):
        self.time = None

    def takePoolKey(self,ele):
        return ele.realtime

    def startTimer(self,Mytimer1):
        self.pool.append(Mytimer1)
        self.pool.sort(key=self.takePoolKey)
        self._dealTimerFunc()
        self._timerStart()

    def _timerStart(self):
        if self.time is not None :
            self.time.cancel()
            self.time = None
        if(len(self.pool) == 0):
            return
        self.time = threading.Timer(getDelay(self.pool[0].realtime), self.timerFunc, [self.pool[0]])
        self.time.start()

    def _dealTimerFunc(self):
        for Mytimer1 in self.pool:
            if(Mytimer1.realtime <= time.time()):
                sendMsgself(Mytimer1.MyMsgPkg)
                if(Mytimer1.isCycle == 1 and Mytimer1.sec > 0):
                    Mytimer1.realtime = Mytimer1.realtime + Mytimer1.sec
                else:
                    self.pool.remove(Mytimer1)
            else:
                break
        self.pool.sort(key=self.takePoolKey)

    def timerFunc(self,Mytimer1):
        self._dealTimerFunc()
        self._timerStart()

