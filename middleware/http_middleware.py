import json
import time

from monitor.models import HttpRecord

class HttpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        s_time = time.time()
        response = self.get_response(request)
        e_time = time.time()
        c_time = round(e_time - s_time, 2)

        http_record = HttpRecord(
            host=request.get_host(),
            path=request.get_full_path_info(),
            method=request.method,
            body=json.dumps(json.loads(request.body.decode('utf-8')), ensure_ascii=False) if request.body.decode('utf-8') else None,
            cost_time=c_time
        )
        http_record.save()

        return response