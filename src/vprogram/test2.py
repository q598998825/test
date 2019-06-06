# coding=utf-8
from mycomm import *
import logging

def Init():
    logging.debug("test2 Init")
    return 0


def Proc(msg):
    logging.debug("test2 Proc")
