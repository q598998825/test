from globalConfig import *
from mysingleton import *
import sqlite3



def myDataBaseInit():
    myDatabseMng()
    return 0

def myDataBaseProc():
    pass

@singleton
class myDatabseMng():
    def __init__(self):
        self.conn = sqlite3.connect(GetGlobalConfig()["database"]["datafile"])
        self.conn.row_factory  = sqlite3.Row
        print("Opened database successfully")
