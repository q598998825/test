from mydatabase import *
from mydatabase import *

class tb_things(mydatabase_table):
    table_infos = {"ai_things":{"table_name":"ai_things",
                                "desc":"描述事物的表",
                                "table_col":[{"col":"ID","opt":" NUMBER NOT NULL"},  #可共用，共用意味着指向同一事物
                                             {"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},  #唯一，复用名称不一样
                                             {"col":"TYPE","opt":" VARCHAR(32) NOT NULL"},  #类型，事物的类型
                                             {"col": "STATE", "opt": "NUMBER "},            # 1伪正常数据，0或无没数据
                                             {"col":"DESC","opt":" VARCHAR(128) NOT NULL"}  #注释
                                             ]},
                   "ai_actions": {"table_name": "ai_actions",
                                 "desc": "描述事物的行为",
                                 "table_col": [{"col": "THINGS_ID", "opt": " NUMBER NOT NULL"},             # 可共用，共用意味着指向同一事物
                                               {"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                               # 唯一，复用名称不一样
                                               {"col": "TYPE", "opt": " VARCHAR(32) NOT NULL"},  # 类型，事物的类型
                                               {"col": "STATE", "opt": "NUMBER "},  # 1伪正常数据，0或无没数据
                                               {"col": "DESC", "opt": " VARCHAR(128) NOT NULL"}  # 注释
                                               ]}
                   }
    defaultSql = {}  # 常用语句制作
    def __init__(self,cursor):
        super().__init__(cursor)
        self.Init()