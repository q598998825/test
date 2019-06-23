# coding=utf-8
from mycomm import *
from mymsg import *
import logging

def Init():
    logging.debug("test2 Init")
    MyMsgPkg1 =MyMsgPkg()
    MyMsgPkg1.To = "test1"
    MyMsgPkg1.Data = "123213123"
    sendMsgself(MyMsgPkg1)
    sendMsgself(MyMsgPkg1)
    return 0


def Proc(msg):
    logging.debug("test2 Proc")
