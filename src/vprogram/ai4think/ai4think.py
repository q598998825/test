import logging
from mymsg import *
from ai4thinkDm import *
from mydatabase import *

def Init():
    logging.debug("ai4think Init")
    mydatabase1 = mydatabase()
    tb_things1 = tb_things(mydatabase1)
    tb_cm_things1 = tb_cm_things(mydatabase1)
    tb_things1.Init()
    tb_cm_things1.Init()
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("ai4think Proc %s"%(msg.Data))


