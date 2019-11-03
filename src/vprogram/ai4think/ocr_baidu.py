from aip import AipOcr
from mymsg import *
import logging
ocr_baidu = None

def Proc(msg:MyMsgPkg):
    pass

class ocr_baidu():
    def __init__(self):
        """ 你的 APPID AK SK """
        APP_ID = '17678666'
        API_KEY = '1EUtGskaDosUfoHqRilUkiW7'
        SECRET_KEY = '6ZkcxL4etsOgswxe9IzzBmjvXbZsNQZp'
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def basicGeneral(self,img):
        test = self.client.basicGeneral(img)
        logging.debug("basicGeneral:test:%s"%test)
        return test