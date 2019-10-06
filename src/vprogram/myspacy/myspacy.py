import jieba, logging, jieba.posseg
from mymsg import *
def Init():
    logging.debug("myspacy Init")
    seg_list = jieba.posseg.cut("循环处理数据")
    for i in seg_list:
        logging.debug("{}/{},".format(i.word,i.flag))  # 全模式
    logging.debug("myspacy Init end")
    return 0

def Proc(msg:MyMsgPkg):
    logging.debug("myspacy Proc %s"%(msg.Data))