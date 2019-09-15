import json

g_BaseConfig = None

def globalConfigInit():
    MySysConfig = "./mysys/config/config.json"
    global g_BaseConfig

    file = open(MySysConfig, 'r', encoding='utf-8')
    g_BaseConfig = json.load(file)
    return 0

def GetGlobalConfig():
    global g_BaseConfig
    return g_BaseConfig