import logging
from mymsg import *
from ai4thinkDm import *
from mydatabase import *
from makeProgram import *
from input import *
from ocr_baidu import *

def Init():
    logging.debug("ai4think Init")
    mydatabase1 = mydatabase()
    tb_things1 = tb_things(mydatabase1)
    tb_cm_things1 = tb_cm_things(mydatabase1)
    tb_things1.Init()
    tb_cm_things1.Init()
    mydatabase2 = mydatabase()
    loadProgram1 = loadProgram(mydatabase2)
    ocr_baidu1 = ocr_baidu()
    #loadProgram1.Init()
    loadProgram1.load("GetScreen")
    #with open("123.jpg", 'rb') as fp:
    #    img=fp.read()
    #ocr_baidu1.basicGeneral(img)
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("ai4think Proc %s"%(msg.Data))