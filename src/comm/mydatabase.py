from mydatabasemng import *
from mysingleton import *
import logging

class mydatabase():
    def __init__(self):
        self.cursor = myDatabseMng().conn.cursor()

    def __del__(self):
        self.cursor.close()

    def commit(self):
        self.cursor.commit()

    def rollback(self):
        self.cursor.rollback()

class mydatabase_table():
    table_name = ""
    table_col = []
    def __init__(self,mydatabase:mydatabase):
        self.database = mydatabase
        pass

    def execSql(self,sql):
        logging.debug(sql)
        return self.database.cursor.execute(sql)

    def Bind(self,key,value):
        pass

    def checkTableExist(self):
        cursor = self.execSql("SELECT 1 FROM sqlite_master WHERE type='table' and name = '%s'"%self.table_name)
        for i in cursor:
            return True
        return False


    def Init(self):
        if(False == self.checkTableExist()):
            self.CreateTable()

    def col2str(self):
        tmp = ""
        for i in self.table_col:
            if (("col" in i ) and ("opt" in i)):
                if 0 == len(tmp):
                    tmp = i["col"] + " "+ i["opt"]
                else:
                    tmp += ", " + i["col"] + " " + i["opt"]
        return tmp

    def CreateTable(self):
        self.execSql("CREATE TABLE %s (%s)" % (self.table_name,self.col2str()))