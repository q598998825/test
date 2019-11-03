import  logging
from mydatabase import *
from mycomm import *

class commCode(mydatabase_table):
    table_infos = {"code_var":{"table_name":"code_var",
                                "desc":"描述代码的变量",
                                "table_col":    [{"col":"name", "opt": " VARCHAR(64)"},
                                                {"col": "type", "opt": " VARCHAR(64)"},
                                                {"col":"istatic","opt":" NUMBER"},
                                                {"col": "subsclass", "opt": "VARCHAR(64) "},
                                                {"col": "declare_file", "opt": "VARCHAR(512)"},
                                                {"col": "declare_line", "opt": "VARCHAR(32)"},
                                                {"col": "real_file", "opt": "VARCHAR(512)"},
                                                {"col": "real_line", "opt": "VARCHAR(32)"},
                                                {"col":"DESC","opt":" VARCHAR(128)"}
                                                ]},
                   "code_function": {"table_name": "code_function",
                                "desc": "描述代码的函数",
                                "table_col": [{"col": "name", "opt": " VARCHAR(64)"},
                                              {"col": "type", "opt": " VARCHAR(64)"},
                                              {"col": "istatic", "opt": " NUMBER"},
                                              {"col": "return_type", "opt": " VARCHAR(64)"},
                                              {"col": "subsclass", "opt": "VARCHAR(64) "},
                                              {"col": "declare_file", "opt": "VARCHAR(512)"},
                                              {"col": "declare_line", "opt": "VARCHAR(32)"},
                                              {"col": "real_file", "opt": "VARCHAR(512)"},
                                              {"col": "real_line", "opt": "VARCHAR(32)"},
                                              {"col": "DESC", "opt": " VARCHAR(256)"}
                                              ]},
                   "code_param": {"table_name": "code_param",
                                     "desc": "描述代码的函数",
                                     "table_col": [{"col": "name", "opt": " VARCHAR(64)"},
                                                   {"col": "type", "opt": " VARCHAR(64)"},
                                                   {"col": "istatic", "opt": " NUMBER"},
                                                   {"col": "subsclass", "opt": "VARCHAR(64) "},
                                                   {"col": "declare_file", "opt": "VARCHAR(512)"},
                                                   {"col": "declare_line", "opt": "VARCHAR(32)"},
                                                   {"col": "real_file", "opt": "VARCHAR(512)"},
                                                   {"col": "real_line", "opt": "VARCHAR(32)"},
                                                   {"col": "DESC", "opt": " VARCHAR(128)"}
                                                   ]},
                   }
    def __init__(self,cursor):
        super().__init__(cursor)

    def LoadFromPy(self,projectdir):
        filelist = []
        dir_list = []
        get_file_path(projectdir,filelist,dir_list)

