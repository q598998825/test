# coding=utf-8
import logging,socket

class vpro_http:
    def __init__(self):#子类统一初始化
        pass

    def http(self):
        # 获取参数
        tmpMap = self.socketGetVar(str)
