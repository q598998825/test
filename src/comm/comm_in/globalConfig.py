import json,threading

# 创建全局ThreadLocal对象:
lThreadPool = threading.local()
lThreadPool.opcode = "Init"
g_BaseConfig = None

def globalConfigInit():
    MySysConfig = "./mysysdir/config/config.json"
    global g_BaseConfig

    file = open(MySysConfig, 'r', encoding='utf-8')
    g_BaseConfig = json.load(file)
    return 0

def GetGlobalConfig():
    global g_BaseConfig
    return g_BaseConfig
