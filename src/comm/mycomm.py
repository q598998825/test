# coding=utf-8

def for_inStr(str,strArr):
    for tmp in strArr:
        if(str in tmp):
            return tmp
    return None

def strIsNone(str):
    if(str is None or len(str) <= 0):
        return True
    return False