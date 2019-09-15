# coding=utf-8
from mycomm import *
from mymsg import *
from mytimer import *
import logging
from othello import *
from mydatabase import *

def Init():
    #Game().run()
    test123()
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("test1 Proc %s"%(msg.Data))

class test123(mydatabase_table):
    def __init__(self):
        cursor = mydatabase()
        super().__init__(cursor)
        self.table_name = "test_table"
        self.table_col = [{"col":"test1","opt":" INT NOT NULL"},{"col":"test2","opt":" INT NOT NULL"}]
        self.Init()