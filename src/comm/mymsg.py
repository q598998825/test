# coding=utf-8
from mypthread import *
from mysocket import *
import logging
class mymsg():
    pass

class MyMsgPkg():
    def __init__(self):
        self.From = None
        self.To = None
        self.Data = None
        self.id = None

def NativeCall(req,rsp):
    return 0

def sendMsgself(MymsgPkg):
    return