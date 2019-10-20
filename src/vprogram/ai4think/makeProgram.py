from mydatabase import *

TYPE_PROGRAM_PY = "programPy"

class loadProgram(mydatabase_table):
    table_infos = {"ai_program": {"table_name": "ai_program",
                                 "desc": "程序定义表",
                                 "table_col": [{"col": "program_id", "opt": " VARCHAR(64) PRIMARY KEY NOT NULL"},
                                               {"col": "TYPE", "opt": " VARCHAR(64)"},
                                               {"col": "FILE", "opt": "VARCHAR(256)"},
                                               {"col": "CLASS", "opt": "VARCHAR(256) "},
                                               {"col": "FUNC", "opt": "VARCHAR(256)"},
                                               {"col": "STATE", "opt": "NUMBER"},
                                               {"col": "DESC", "opt": " VARCHAR(128)"}  # 注释
                                               ]}
                   }
    def Init(self):
        super().Init()


    def load(self,program_id):
        pass



class makeProgram(mydatabase_table):
    def Init(self):
        if self.CheckHasInit():
            return
        self.programInit()


    def CheckHasInit(self):
        global NUM_PROGRAM_MAKE_START
        cursor = self.execSql("SELECT 1 FROM ai_things WHERE ID=10000 ")
        return self.checkHasResult(cursor)

    def programInit(self):
        global TYPE_PROGRAM_PY
        tmpNum = NUM_PROGRAM_MAKE_START
        self.execSql("INSERT INTO ai_things (ID, NAME, TYPE, STATE, DESC) VALUES('10000' ,'编程', '%s', 1, '事物描述')"%(TYPE_PROGRAM_PY))
        self.execSql("INSERT INTO cm_ai_things (ID, NAME, STATE, DESC) VALUES('10000' ,'python', '%s', 1, '事物描述')" % (TYPE_PROGRAM_PY))
        self.execSql("INSERT INTO cm_ai_actions (NAME, THINGS_ID, TYPE, VALUE, ISACTIVE, STATE, DESC) \
        VALUES('循环','10000','%s','loop', -1, 1, '调用循环处理程序')"%TYPE_PROGRAM_PY)

    def loop(self):
        pass
