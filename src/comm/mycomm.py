# coding=utf-8
import logging,time,os

def for_inStr(str,strArr):
    for tmp in strArr:
        if(str in tmp):
            return tmp
    return None

def strIsNone(str):
    if(str is None or len(str) <= 0):
        return True
    return False

def getDelay(time1):
    return time1 - time.time()

def get_file_path(self,path, file_list, dir_list):
    dir_list.append(path)
    self.get_file_path_in(path, file_list, dir_list)

def get_file_path_in(self,path, file_list, dir_list):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(path)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(path, dir_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            # 递归获取所有文件和目录的路径
            self.get_file_path_in(dir_file_path, file_list, dir_list)
        else:
            file_list.append(dir_file_path)