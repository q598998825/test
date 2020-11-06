from django.http import HttpResponse
import logging

def hello(request):
    logging.debug("hello begin")
    return HttpResponse(\
        '{"cutOffDay":"20201023","providePartyID":"ctbsgd9980","response":{"rspCode":"30000","rspDesc":"业务处理失败"},"result":"{\\"OprSeq\\":\\"2009992020102211375249090487\\",\\"OrderSeq\\":\\"1603423493174992699769260844721\\",\\"BizCode\\":\\"3999\\",\\"BizDesc\\":\\"其它错误:待创建的组织机构父埗组织不存在。\\"}","transIDH":"2009992020102211375249090487","transIDHTime":"20201023112453","transIDO":"99920201023111158390744922"}')
