import spacy, logging
from mymsg import *

def Init():
    logging.debug("myspacy Init")
    nlp = spacy.load("en")
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("myspacy Proc %s"%(msg.Data))