# coding=utf-8
import logging,os
from vscript_rule import *
from mydatabase import *

class vscript_list(mydatabase_table):

    table_infos = {"vscript_list": {"table_name": "vscript_list",
                                 "desc": "脚本列表",
                                 "table_col": [{"col": "NAME", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                               {"col": "FILENAME", "opt": " VARCHAR(128) NOT NULL"},  # 类型，事物的类型
                                               {"col": "STATE", "opt": "NUMBER "},  # 1为正常数据，0为无没数据
                                               {"col": "DESC", "opt": " VARCHAR(128)"}  # 注释
                                               ]},
                   "tmpData": {"table_name": "tmpData",
                                    "desc": "脚本临时数据列表",
                                    "table_col": [{"col": "KEY", "opt": " VARCHAR(128) PRIMARY KEY NOT NULL"},
                                                  {"col": "VALUE", "opt": " VARCHAR(1024)"},  # 值
                                                  {"col": "updateDate", "opt": "DATE "},  # 更新时间
                                                  {"col": "DESC", "opt": " VARCHAR(128)"}  # 注释
                                                  ]}
                   }

    defaultSql = {"getList":"select NAME,FILENAME,STATE,DESC from vscript_list where state = 1",
                  "getData":"select KEY,VALUE,updateDate,DESC from tmpData where KEY = '%s'",
                  "setData":"insert or replace into tmpData (KEY,VALUE,updateDate) VALUES ('%s',(%s),datetime())"}  # 常用语句制作

    def __init__(self):
        super().__init__()
        self.Init()

    def Init(self):
        super().Init()
        #self.DefaultData()
