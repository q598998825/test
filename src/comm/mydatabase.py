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
    table_infos = {}    #可存复数表信息
    ''' 格式
    {"tableName1":{"table_name":"tableName1","table_col":[{"col":"col1","opt":"opt1"},{"col":"col2","opt":"opt2"}]},
    "tableName2":{"table_name":"tableName2","table_col":[{"col":"col1","opt":"opt1"},{"col":"col2","opt":"opt2"}]}
    }
    '''
    defaultSql = {}     #常用语句制作
    ''' 格式
    {"key1":"sql1",
    "key2":"sql2"}
    '''
    def __init__(self,mydatabase:mydatabase):
        self.database = mydatabase
        pass

    def execSql(self,sql):
        logging.debug(sql)
        return self.database.cursor.execute(sql)

    def Bind(self,key,value):
        pass

    def checkTableExist(self,table_name):
        cursor = self.execSql("SELECT 1 FROM sqlite_master WHERE type='table' and name = '%s'"%table_name)
        for i in cursor:
            logging.debug(chr(i[0]) + ',' + chr(i["1"]))
            return True
        return False

    def checkTableCols(self):
        pass

    def Init(self):
        for tableName in self.table_infos:
            if(False == self.checkTableExist(tableName)):
                self.CreateTable(self.table_infos[tableName])
                logging.debug("test1")
            logging.debug("test2")

    def col2str(self,tableinfo):
        tmp = ""
        for i in tableinfo["table_col"]:
            if (("col" in i ) and ("opt" in i)):
                if 0 == len(tmp):
                    tmp = i["col"] + " "+ i["opt"]
                else:
                    tmp += ", " + i["col"] + " " + i["opt"]
        return tmp

    def CreateTable(self,tableInfo):
        self.execSql("CREATE TABLE %s (%s)" % (tableInfo["table_name"],self.col2str(tableInfo)))

    def useDefaultSql(self,sqlKey):
        if sqlKey not in self.defaultSql:
            logging.error("it does't has this key in defaultSql")
            return -1

        return self.execSql(self.defaultSql[sqlKey])

