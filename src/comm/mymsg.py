# coding=utf-8
from mypthread import *
from mysocket import *
from mysysdir.mysys import *
import logging
class mymsg():
    pass

class MyMsgPkg():
    def __init__(self):
        self.From = None
        self.To = None
        self.Data = None
        self.FromId = None
        self.ToId = None
        self.id = None

def NativeCall(req,rsp):
    return 0

def sendMsgself(MymsgPkg):
    mysys1 = mysys()
    mysys1.sendmsg(MymsgPkg)
    return
