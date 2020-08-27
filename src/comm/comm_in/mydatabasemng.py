from globalConfig import *
from mypthread import lThreadPool
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
        self.conn = {}
        #self.lock = threading.RLock()
        '''
        for i in range(self.maxConnNum):
            self.conn.append(mydatabase_in())
            self.conn[i].conn = sqlite3.connect(GetGlobalConfig()["database"]["datafile"])
            self.conn[i].id = i
            self.conn[i].conn.row_factory  = sqlite3.Row
        '''
        print("Opened database successfully")

    def GetConn(self):
        #self.lock.acquire()
        #conn = None

        if lThreadPool.opcode not in self.conn:
            self.conn[lThreadPool.opcode] = mydatabase_in()
            self.conn[lThreadPool.opcode].conn = sqlite3.connect(GetGlobalConfig()["database"]["datafile"])
            self.conn[lThreadPool.opcode].conn.row_factory = sqlite3.Row
        #self.lock.release()
        return self.conn[lThreadPool.opcode]

    def FreeConn(self,conn):
        conn.commit()

        #self.lock.acquire()
        #self.conn[conn.id].state = True
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
