# encoding: utf-8

import socket

class mysock():
    sock = None
    type = None


class mysocket():
    def __init__(self):
        self.FucMap = {"TCP":{"init":self.tcpInit,'send':self.tcpSend,'recv':self.tcpRecv},
                       "UDP":{"init":self.udpInit,'send':self.udpSend,'recv':self.udpRecv}}
        pass

    def sockInit(self,type = "TCP",ip = "localhost", port = 0,IsClient = True):
        sock = None
        if(type in self.FucMap):
            sock = self.FucMap[type]["init"](ip,port,IsClient)
        return sock

    def send(self,Socket,data,datalen,timeout = 30):
        if(Socket.type not in self.FucMap):
            print("no type socket[%s]"%Socket.type)
            return None
        return self.FucMap[Socket.type]["send"](Socket,data,datalen,timeout)

    def recv(self,Socket,data,datalen,timeout = 30):
        pass

    def checkIpPort(self,ip,port):
        if(ip != "localhost" or port != 0):
            return True
        return False

    def tcpInit(self,ip = "localhost", port = 0,IsClient = True):
        sockval = mysock()
        sockval.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockval.type = "TCP"
        if(IsClient):
            if (self.checkIpPort(ip, port) == False):
                return None
            sockval.sock.connect((ip, port))
        else:
            if(self.checkIpPort(ip, port) == False):
                return None
            sockval.sock.bind((ip,port))
        sockval.sock.setblocking(False)
        return sockval
    def tcpSend(self,Socket,data,datalen,timeout = 30):
        Socket.sock.send()
        pass
    def tcpRecv(self,Socket,data,datalen,timeout = 30):
        pass

    def udpInit(self,ip = None, port = None,IsClient = True):
        pass
    def udpSend(self,Socket,data,datalen,timeout = 30):
        pass
    def udpRecv(self,Socket,data,datalen,timeout = 30):
        pass

if __name__=="__main__":
    mysocket1 = mysocket()
    socket1 = mysocket1.sockInit(ip="100.101.89.238",port= 82)
    if(socket1 is None):
        print("分配失败")

    pass
