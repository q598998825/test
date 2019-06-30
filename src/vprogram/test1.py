# coding=utf-8
from mycomm import *
from mymsg import *
from mytimer import *
import logging
def Init():
    logging.debug("test1 Init")
    myTimer1=myTimer('from1','test1','msg1',1)
    myTimer2 = myTimer('from2', 'test1', 'msg2', 2)
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("test1 Proc %s"%(msg.Data))
