# common imports
import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from common.utils import CommonUtils
from common.logger import info_log, error_log

from user.serializer import UserSerializer
from user.models import User


# Create your views here.
class UserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        info_log(request, 'UserView get')
        try:
            user = User.objects.get(id=11)
        except Exception:
            error_log(request)

        data = json.loads(request.body).get('data', None) if request.body else None
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return CommonUtils.dispatch_success(request, serializer.data)
