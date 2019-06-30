# coding=utf-8
from mycomm import *
from mymsg import *
import logging
from mytimer import *

def Init():
    logging.debug("test2 Init")
    MyMsgPkg1 =MyMsgPkg()
    MyMsgPkg1.To = "test1"
    MyMsgPkg1.Data = "123213123"
    sendMsgself(MyMsgPkg1)
    sendMsgself(MyMsgPkg1)
    myTimer1 = myTimer('from1', 'test1', 'msg1', 1)
    myTimer2 = myTimer('from2', 'test1', 'msg2', 2)
    return 0


def Proc(msg:MyMsgPkg):
    logging.debug("test2 Proc")
