# coding=utf-8
from mytimermng import *
from mymsg import *
import logging,time

def SleepTime2RealTime(sec:float):
    time_now = time.time() + sec
    return time_now

class myTimer():
    def __init__(self,from1 ,to1, msg1, sec :float, flag:int = 0,isCycle:int = 0):
        self.sec = sec          #flag为0时传秒，否则传time
        self.isCycle = isCycle
        self.realtime = None    #给定时器管理组用
        self.flag = flag #0,普通延时，time毫秒级，1，以时间节点延时
        self.MyMsgPkg = MyMsgPkg()
        self.MyMsgPkg.From = from1
        self.MyMsgPkg.To = to1
        self.MyMsgPkg.Data = msg1
        self.MyMsgPkg.FromId = 'timer'
        if(0 > self.Init4Mng()):
            logging.error("参数有误，timer初始化失败")
            pass
        myTimerMng1=myTimerMng()
        myTimerMng1.startTimer(self)

    def Init4Mng(self):
        if(self.flag == 0):
            if self.sec <0:
                if(self.isCycle == 1):
                    self.sec = 0-self.sec
            self.realtime = SleepTime2RealTime(self.sec)
        else:
            #暂时不支持
            #if self.sec <= time.time() and self.isCycle == 0:
                #logging.error("定时器不允许延时过去的时间[%s]"%self.sec)
            return -1
            #self.realtime = self.sec
        return 0