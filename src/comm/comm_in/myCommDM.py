from mydatabase import *


class comm_param(mydatabase_table):

    table_infos = {"comm_param": {"table_name": "comm_param",
                                 "desc": "参数列表",
                                 "table_col": [{"col": "key", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                               {"col": "value", "opt": " VARCHAR(256) NOT NULL"},  # 类型，事物的类型
                                               {"col": "STATE", "opt": "NUMBER "},  # 1为正常数据，0为无没数据
                                               {"col": "DESC", "opt": " VARCHAR(256)"}  # 注释
                                               ]},
                   }

    defaultSql = {"getValue":"select VALUE from comm_param where key = '%s' and state = 1"}  # 常用语句制作

    def __init__(self):
        super().__init__()
        self.Init()

    def Init(self):
        super().Init()

def Init():
    logging.debug("myCommDM Init")
    comm_param()
    logging.debug("myCommDM Init end")
    return 0

def Proc(msg):
    pass
