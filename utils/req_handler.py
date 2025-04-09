# utils/decorators.py
from functools import wraps
from django.http import JsonResponse, HttpResponse

def req_handler(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            # 执行视图函数
            result = func(request, *args, **kwargs)

            # 处理普通HttpResponse
            return JsonResponse({
                'code': 200,
                'msg': 'success',
                'data': result
            })

        except Exception as e:
            # 异常时统一返回格式
            error_data = {
                'code': 500,
                'msg': 'error',
                'data': str(e)
            }
            return JsonResponse(error_data, status=500)

    return wrapper