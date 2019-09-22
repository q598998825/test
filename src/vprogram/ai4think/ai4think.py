import logging
from mymsg import *
from ai4thinkDm import *


def Init():
    logging.debug("ai4think Init")
    tb_things1 = tb_things();
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("ai4think Proc %s"%(msg.Data))


