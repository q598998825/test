# coding=utf-8
from mycomm import *
from mymsg import *
from mytimer import *
import logging
from othello import *
from mydatabase import *

def Init():
    #Game().run()
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("test1 Proc %s"%(msg.Data))