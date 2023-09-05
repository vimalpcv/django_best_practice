from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user.serializer import UserSerializer
from user.models import User

from rest_framework import status
from rest_framework.response import Response


# Create your views here.
class UserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
