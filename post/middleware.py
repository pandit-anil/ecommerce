from .models import Systemsetting

class SystemSettingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.system_setting = Systemsetting.objects.first()
        response = self.get_response(request)
        return response