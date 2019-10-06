from globalConfig import *
from mysingleton import *
import sqlite3, threading



def myDataBaseInit():
    myDatabseMng()
    return 0

def myDataBaseProc():
    pass

@singleton
class myDatabseMng():
    maxConnNum = 20
    def __init__(self):
        self.conn = []
        #self.lock = threading.RLock()

        for i in range(self.maxConnNum):
            self.conn.append(mydatabase_in())
            self.conn[i].conn = sqlite3.connect(GetGlobalConfig()["database"]["datafile"])
            self.conn[i].id = i
            self.conn[i].conn.row_factory  = sqlite3.Row
        print("Opened database successfully")

    def GetConn(self):
        #self.lock.acquire()
        conn = None
        for i in range(self.maxConnNum):
            if(self.conn[i].state):
                self.conn[i].state = False
                conn = self.conn[i]
                break
        #self.lock.release()
        return conn

    def FreeConn(self,conn):
        if conn.id <0 or conn.id > self.maxConnNum:
            return
        conn.commit()

        #self.lock.acquire()
        self.conn[conn.id].state = True
        #self.lock.release()

class mydatabase_in():
    conn = None
    state = True
    id = -1
    def __init__(self):
        pass

    def __del__(self):
        self.commit()

    def commit(self):
        if self.state == True :
            self.conn.commit()

    def rollback(self):
        self.conn.rollback()