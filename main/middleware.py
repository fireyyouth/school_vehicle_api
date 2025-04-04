from django.utils.deprecation import MiddlewareMixin

class PrintHeadersMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("Request Headers:")
        for key, value in request.headers.items():
            print(f"{key}: {value}")
