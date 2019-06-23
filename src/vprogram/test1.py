# coding=utf-8
from mycomm import *
import logging
def Init():
    logging.debug("test1 Init")
    return 0

def Proc(msg):
    logging.debug("test1 Proc")
