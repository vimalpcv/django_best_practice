# common imports
import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from common.utils import CommonUtils
from common.logger import info_log, error_log
from common.error import *
from user.serializer import UserSerializer
from user.models import User


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # info_log(request, 'LoginView post')
        try:
            data = request.data.get('data', None)
            if not data:
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS,
                                                    error_message='data is missing')
            username = data.get('username', None)
            password = data.get('password', None)
            if not username or not password:
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS,
                                                    error_message='username or password is missing')

            user = authenticate(username=data['username'], password=data['password'])
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                data = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                }
            return CommonUtils.dispatch_success(request, data)
        except Exception:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)


# Create your views here.
class UserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def put(self, request):


        info_log(request, 'UserView get')
        print(request.POST.get('file'))
        try:
            user = User.objects.get(id=11)
        except Exception:
            error_log(request)

        data = json.loads(request.body).get('data', None)
        print('view data', data)
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return CommonUtils.dispatch_success(request, serializer.data)
