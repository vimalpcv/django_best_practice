from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .utils import CommonUtils


class HealthCheck(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        print('HealthCheck')
        return CommonUtils.dispatch_success(request, 'OK')
