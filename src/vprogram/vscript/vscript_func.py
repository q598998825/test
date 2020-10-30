# coding=utf-8
import logging
from mymsg import *
from vscript import *
from vscript_dm import *

def Init():
    logging.debug("vscript_func Init")
    vscript_list()
    vscript1=vscript()
    vscript1.run()
    logging.debug("vscript_func Init end")
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("vscript_func Proc %s"%(msg.Data))
