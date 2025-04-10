# -*- coding: utf-8 -*-
from ping3 import ping
from utils.req_handler import req_handler

@req_handler
def ping_test(request):

    if request.method != 'GET':
        raise Exception('请求方式有误')

    host = request.GET.get('host')

    # 访问正常返回 float, 不存在站点返回 False, 超时返回 None
    return ping(host)