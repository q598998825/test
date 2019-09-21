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
    table_infos = {}  # 可存复数表信息
    ''' 格式
    {"tableName1":{"table_name":"tableName1","table_col":[{"col":"col1","opt":"opt1"},{"col":"col2","opt":"opt2"}]},
    "tableName2":{"table_name":"tableName2","table_col":[{"col":"col1","opt":"opt1"},{"col":"col2","opt":"opt2"}]}
    }
    '''
    defaultSql = {}  # 常用语句制作
    ''' 格式
    {key1:sql1,
    key2:sql2}
    '''
    def __init__(self):
        cursor = mydatabase()
        super().__init__(cursor)
        self.table_infos = {"test_table":{"table_name":"test_table","table_col":[{"col":"test1","opt":" INT NOT NULL"},{"col":"test2","opt":" INT NOT NULL"}]}}
        self.Init()