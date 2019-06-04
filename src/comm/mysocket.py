# coding=utf-8
import socket,time,select,queue
from mypthread import *

#基础节点
class mysock():
    sock = None
    type = None
    func = None

#基础socket
class mysocket():
    def __init__(self):
        self.FucMap = {"TCP":{"init":self.tcpInit,'send':self.tcpSend,'recv':self.tcpRecv},
                       "UDP":{"init":self.udpInit,'send':self.udpSend,'recv':self.udpRecv}}
        pass

    def sockInit(self,type = "TCP",ip = "localhost", port = 0,timeout = 30,IsClient = True,listennum = 1024):
        sock = None
        if(type in self.FucMap):
            sock = self.FucMap[type]["init"](ip,port,timeout,IsClient,listennum)
        return sock

    def send(self,Socket,data,addr,timeout = 30):
        if(Socket.type not in self.FucMap):
            print("no type socket[%s]"%Socket.type)
            return None
        return self.FucMap[Socket.type]["send"](Socket,data,addr,timeout)

    def recv(self,Socket,addr, size = 1024,timeout = 30):
        pass

    def checkIpPort(self,ip,port):
        if(ip != "localhost" or port != 0):
            return True
        return False

    def tcpInit(self,ip = "localhost", port = 0,timeout = 30,IsClient = True,listennum = 1024):
        sockval = mysock()
        sockval.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockval.type = "TCP"
        sockval.sock.settimeout(timeout)

        if(IsClient):
            if (self.checkIpPort(ip, port) == False):
                return None
            sockval.sock.connect((ip, port))
        else:
            if(self.checkIpPort(ip, port) == False):
                return None
            sockval.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sockval.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sockval.sock.bind((ip,port))
            sockval.sock.listen(listennum)
        sockval.sock.setblocking(False)

        return sockval
    def tcpSend(self,Socket,data,addr):
        return Socket.sock.sendall(data)

    def tcpRecv(self,Socket,addr, size = 1024):
        return Socket.sock.recv(1024)


    def udpInit(self,ip = None, port = None,timeout = 30,IsClient = True,listennum = 1024):
        pass
    def udpSend(self,Socket,data,addr):
        pass
    def udpRecv(self,Socket,addr, size = 1024):
        pass

#基础socket池
class mysocketServerPool():
    pool = {}
    client_pool = {}
    mypthread1 = None
    sleepTime = 30
    inputs = []  # select 接收文件描述符列表
    outputs = []  # 输出文件描述符列表
    message_queues = {}  # 消息队列
    client_info = {}
    bufsize = 1024
    def __init__(self):
        self.FucMap = {"TCP":{"add":self.addTcpSocket,'del':self.delTcpSocket},
                       "UDP":{"add":self.addTcpSocket,'del':self.delTcpSocket}}

    def addSocket(self,socket1,Func):
        if(True != isinstance(socket1,mysock)):
            print("socket[%s]对象实例异常"%socket)
            return
        if(socket1.type not in self.FucMap):
            print("服务池不适配于此类型socket[%s]"%socket1.type)
        if(Func is not None):
            socket1.func = Func
        self.FucMap[socket1.type]["add"](socket1)
        self.inputs.append(socket1.sock)
        self.pool[socket1.sock] = socket1

    def delSocket(self,socket):
        if(socket in self.pool):
            self.FucMap[self.pool[socket].type]["del"](socket)
        self.closesocket(socket)

    def addTcpSocket(self,socket1):
        pass

    def delTcpSocket(self,socket1):
        pass

    def Func(self,arg):
        while (True):
            if(len(self.pool) <= 0):
                time.sleep(self.sleepTime)
                continue
            #监听
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, self.sleepTime)
            if not (readable or writable or exceptional) :
                continue
            #处理socket
            self.dealReadable(readable)
            self.dealwritable(writable)
            self.dealexceptional(exceptional)


    def run(self):
        if None is self.mypthread1:
            self.mypthread1 = mypthread(self.Func,None)
            self.mypthread1.start()

    def dealReadable(self,readable):
        for s in readable:
            if s in self.pool:#是客户端链接
                connection, client_address = s.accept()
                # print "connection", connection
                print("%s connect." % str(client_address))
                connection.setblocking(0)  # 非阻塞
                self.inputs.append(connection)  # 客户端添加到inputs
                self.client_info[connection] = str(client_address)
                self.message_queues[connection] = queue.Queue()  # 每个客户端一个消息队列
                self.client_pool[connection] = self.pool[s]
            else:#是client, 数据发送过来
                try:
                    data = s.recv(self.bufsize)
                except:
                    print("Client Error!")
                if data:
                    data = "%s %s say: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), self.client_info[s], data)
                    if(self.client_pool[s].func is not None):
                        self.client_pool[s].func(self,s,data)
                else:  # 客户端断开
                    print("Client:%s Close." % str(self.client_info[s]))
                    self.closesocket(s)

        pass
    def dealwritable(self,writable):
        for s in writable:  # outputs 有消息就要发出去了
            try:
                next_msg = self.message_queues[s].get_nowait()  # 非阻塞获取
            except queue.Empty:
                print("Output Queue is Empty!")
            except Exception as e:  # 发送的时候客户端关闭了则会出现writable和readable同时有数据，会出现message_queues的keyerror
                print("Send Data Error! ErrMsg:%s" % str(e))
                self.closesocket(s)
            else:
                try:
                    s.sendall(next_msg)
                except Exception as e:  # 发送失败就关掉
                    print("Send Data to %s  Error! ErrMsg:%s" % (str(self.client_info[s]), str(e)))
                    print("Client: %s Close Error." % str(self.client_info[s]))
                    self.closesocket(s)

    def dealexceptional(self,exceptional):
        for s in exceptional:
            print("Client:%s Close Error." % str(self.client_info[s]))
            self.closesocket(s)

    def closesocket(self,sock):
        if sock in self.inputs:
            self.inputs.remove(sock)
            sock.close()
        if sock in self.outputs:
            self.outputs.remove(sock)
        if sock in self.message_queues:
            del self.message_queues[sock]
        del self.client_info[sock]
        if(sock in self.pool):
            del self.pool[sock]
        if(sock in self.client_pool):
            del self.client_pool[sock]

    def resoponse(self,s,data):
        if s not in self.outputs:  # 要回复消息
            self.outputs.append(s)
        self.message_queues[s].put(data)
