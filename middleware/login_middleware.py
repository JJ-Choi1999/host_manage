from django.middleware.csrf import CsrfViewMiddleware

class LoginMiddleware(CsrfViewMiddleware):

    def __init__(self, get_response):
        self.__get_response = get_response
        super().__init__(self.__get_response)

    def __call__(self, request):
        response = self.__get_response(request)
        return response