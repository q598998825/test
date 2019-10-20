from mydatabase import *
from mydatabase import *

class tb_things(mydatabase_table):
    table_infos = {"ai_things":{"table_name":"ai_things",
                                "desc":"描述事物的表",
                                "table_col":    [{"col": "ID", "opt": " NUMBER"},
                                                {"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},            #唯一，复用名称不一样
                                                {"col":"TYPE","opt":" VARCHAR(32) NOT NULL"},                           #类型，事物的类型
                                                {"col": "STATE", "opt": "NUMBER "},                                     # 1为正常数据，0为无没数据
                                                {"col":"DESC","opt":" VARCHAR(128)"}                                    #注释
                                                ]},
                   "ai_attr": {"table_name": "ai_attr",
                                 "desc": "描述事物的属性表",
                                 "table_col": [{"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                               {"col": "ATTR_TYPE", "opt": " VARCHAR(32) NOT NULL"},                    # 类型，事物的类型
                                               {"col": "STATE", "opt": "NUMBER "},                                      # 1为正常数据，0为无没数据
                                               {"col": "DESC", "opt": " VARCHAR(128)"}                                  # 注释
                                               ]},
                   "ai_actions":{"table_name": "ai_actions",
                                "desc": "描述事物的行为",
                                "table_col":    [{"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},            # 唯一，复用名称不一样
                                                {"col": "TYPE", "opt": " VARCHAR(32) NOT NULL"},                        # 类型，事物的类型
                                                #{"col": "VALUE", "opt": " VARCHAR(1024)"},
                                                {"col": "ISACTIVE", "opt": " int NOT NULL"},                            # 主被动
                                                {"col": "STATE", "opt": "NUMBER "},                                     # 1为正常数据，0为无没数据
                                                {"col": "DESC", "opt": " VARCHAR(128)"}                                 # 注释
                                                ]},
                   "ai_actinputs": {"table_name": "ai_actinputs",
                                  "desc": "描述行为输入",
                                  "table_col": [{"col": "ACTION_NAME", "opt": "VARCHAR(64) NOT NULL"},                  # 行为输入
                                                {"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},            # 唯一，复用名称不一样
                                                {"col": "TYPE", "opt": " VARCHAR(32) NOT NULL"},                        # 类型，输入类型
                                                {"col": "STATE", "opt": "NUMBER "},                                     # 1为正常数据，0为无没数据
                                                {"col": "DESC", "opt": " VARCHAR(128)"}                                 # 注释
                                                ]},
                   "ai_actoutputs": {"table_name": "ai_actoutputs",
                                  "desc": "描述行为输出",
                                  "table_col": [{"col": "ACTION_NAME", "opt": "VARCHAR(64) NOT NULL"},                  # 行为输入
                                                {"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},            # 唯一，复用名称不一样
                                                {"col": "TYPE", "opt": " VARCHAR(32) NOT NULL"},                        # 类型，输出类型
                                                {"col": "STATE", "opt": "NUMBER "},                                     # 1为正常数据，0为无没数据
                                                {"col": "DESC", "opt": " VARCHAR(128)"}                                 # 注释
                                                ]}
                   }
    defaultSql = {}  # 常用语句制作
    def __init__(self,cursor):
        super().__init__(cursor)
        #self.Init()
    def Init(self):
        super().Init()
        self.DefaultData()

    def DefaultData(self):
        self.DefaultthingsData()
        pass

    def DefaultthingsData(self):
        cursor = self.execSql("SELECT 1 FROM ai_things WHERE ID=0 ")
        if self.checkHasResult(cursor):
            return
        #接下来加数据
        self.execSql("INSERT INTO ai_things (ID, NAME, TYPE, STATE, DESC) VALUES(0 ,'我', 'things', 1, '事物描述')")
        self.execSql("INSERT INTO ai_things (ID, NAME, TYPE, STATE, DESC) VALUES(1 ,'你', 'things', 1, '事物描述')")
        self.execSql("INSERT INTO ai_things (ID, NAME, TYPE, STATE, DESC) VALUES(2 ,'他', 'things', 1, '事物描述')")

class tb_cm_things(mydatabase_table):
    table_infos = {"cm_ai_things":{"table_name":"cm_ai_things",
                                "desc":"描述事物的表",
                                "table_col":    [{"col": "ID", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                                {"col": "NAME", "opt": " VARCHAR(64)"},                                 #唯一，复用名称不一样
                                                {"col": "STATE", "opt": "NUMBER "},                                     # 1为正常数据，0为无没数据
                                                {"col":"DESC","opt":" VARCHAR(128)"}                                    #注释
                                                ]},
                   "cm_ai_attr": {"table_name": "cm_ai_attr",
                                 "desc": "描述事物的属性表",
                                 "table_col": [{"col": "ID", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                               {"col": "AI_THINGS_ID", "opt": " VARCHAR(64)"},
                                               {"col": "NAME", "opt": " VARCHAR(64)"},
                                               {"col": "VALUE","opt":" VARCHAR(128)"},
                                               {"col": "STATE", "opt": "NUMBER "},                                      # 1为正常数据，0为无没数据
                                               {"col": "DESC", "opt": " VARCHAR(128)"}                                  # 注释
                                               ]},
                   "cm_ai_actions": {"table_name": "cm_ai_actions",
                                  "desc": "行为实例表",
                                  "table_col":    [{"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},            # 唯一，复用名称不一样
                                                {"col": "THINGS_ID", "opt": " VARCHAR(64)"},
                                                {"col": "TYPE", "opt": " VARCHAR(32) NOT NULL"},                        # 类型，事物的类型
                                                {"col": "VALUE", "opt": " VARCHAR(1024)"},
                                                {"col": "ISACTIVE", "opt": " int NOT NULL"},                            # 主被动
                                                {"col": "STATE", "opt": "NUMBER "},                                     # 1为正常数据，0为无没数据
                                                {"col": "DESC", "opt": " VARCHAR(128)"}                                 # 注释
                                                ]},
                   "cm_ai_actinputs": {"table_name": "cm_ai_actinputs",
                                    "desc": "描述行为输入",
                                    "table_col": [{"col": "ACTION_NAME", "opt": "VARCHAR(64) NOT NULL"},  # 行为输入
                                                  {"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                                  {"col": "VALUE", "opt": " VARCHAR(1024)"},
                                                  {"col": "MIN_NUM", "opt": " NUMBER"},                             #0为不限制
                                                  {"col": "MAX_NUM", "opt": " NUMBER"},
                                                  {"col": "STATE", "opt": "NUMBER "},  # 1为正常数据，0为无没数据
                                                  {"col": "DESC", "opt": " VARCHAR(128)"}  # 注释
                                                  ]},
                   "cm_ai_actoutputs": {"table_name": "cm_ai_actoutputs",
                                     "desc": "描述行为输出",
                                     "table_col": [{"col": "ACTION_NAME", "opt": "VARCHAR(64) NOT NULL"},  # 行为输入
                                                   {"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                                   {"col": "VALUE", "opt": " VARCHAR(1024)"},
                                                   {"col": "MIN_NUM", "opt": " NUMBER"},  # 0为不限制
                                                   {"col": "MAX_NUM", "opt": " NUMBER"},
                                                   {"col": "STATE", "opt": "NUMBER "},  # 1为正常数据，0为无没数据
                                                   {"col": "DESC", "opt": " VARCHAR(128)"}  # 注释
                                                   ]}
                   }
    defaultSql = {}  # 常用语句制作
    def __init__(self,cursor):
        super().__init__(cursor)
        #self.Init()

    def Init(self):
        super().Init()
        self.DefaultData()

    def DefaultData(self):
        self.DefaultthingsData()
        pass

    def DefaultthingsData(self):
        cursor = self.execSql("SELECT 1 FROM cm_ai_things WHERE ID=0 ")
        if self.checkHasResult(cursor):
            return
        #接下来加数据
        self.execSql("INSERT INTO cm_ai_things (ID, NAME, STATE, DESC) VALUES(0 ,'我', 1, '事物描述')")
        self.execSql("INSERT INTO cm_ai_things (ID, NAME, STATE, DESC) VALUES(1 ,'你', 1, '事物描述')")
        self.execSql("INSERT INTO cm_ai_things (ID, NAME, STATE, DESC) VALUES(2 ,'他', 1, '事物描述')")