from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import OpenApiParameter, extend_schema
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from functools import partial

from common.utils import CommonUtils
from common.logger import info_log, error_log
from common.permissions import IsAllowedUser
from common.constants import SUPER_ADMIN, ADMIN
from common.error import *
from user.serializer import *
from user.models import User


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        operation_id="Login",
        description="This API is used to create access token and refresh token based on username and password.",
        tags=["General"],
        request=LoginViewSerializer,
        responses={
            200: error_schema,
            400: error_schema,
            500: error_schema,
        }
    )
    def post(self, request):
        try:
            serializer = LoginViewSerializer(data=request.data)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, error_message=serializer.errors)
            else:
                data = serializer.validated_data

            try:
                user = User.objects.select_related("organization").get(username=data['username'])
            except User.DoesNotExist:
                return CommonUtils.dispatch_failure(request, USER_NOT_FOUND,
                                                    error_message=f"User '{data['username']}' not found")

            if not authenticate(username=data["username"], password=data["password"]):
                return CommonUtils.dispatch_failure(request, INVALID_PASSWORD)

            if not user.is_active:
                return CommonUtils.dispatch_failure(request, USER_INACTIVE)

            if not user.organization.is_active:
                return CommonUtils.dispatch_failure(request, ORGANIZATION_INACTIVE)

            refresh = RefreshToken.for_user(user)
            data = {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
            return CommonUtils.dispatch_success(request, data)

        except:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        operation_id="Logout",
        description="This API is used to logout the user.",
        tags=["General"], auth=None,
        request=LogoutViewSerializer,
        responses={
            200: {"type": "object", "properties": {'success': {"type": "string"}}},
            400: error_schema,
            500: error_schema,
        }
    )
    def post(self, request):
        try:
            serializer = LogoutViewSerializer(data=request.data)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, error_message=serializer.errors)
            else:
                data = serializer.validated_data

            try:
                token = RefreshToken(data["refresh_token"])
                token.blacklist()
            except:
                return CommonUtils.dispatch_failure(request, INVALID_REFRESH_TOKEN)
            return CommonUtils.dispatch_success(request, {'success': 'User Logged Out Successfully'})
        except:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)


class RefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)

    @extend_schema(
        operation_id="Refresh Token",
        description="This API is used to refresh the access token.",
        tags=["General"],
        request=RefreshViewSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"}
                }
            },
            400: error_schema,
            500: error_schema,
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = RefreshViewSerializer(data=request.data)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, error_message=serializer.errors)
            data = serializer.validated_data
            request.data["refresh"] = data["refresh_token"]
            try:
                response = super().post(request, *args, **kwargs)
                return CommonUtils.dispatch_success(request, {"access_token": response.data["access"]})
            except:
                return CommonUtils.dispatch_failure(request, INVALID_REFRESH_TOKEN)
        except:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)


class UserDetailView(APIView):
    permission_classes = (partial(IsAllowedUser, SUPER_ADMIN, ADMIN),)
    serializer_class = UserDetailSerializer

    @extend_schema(
        operation_id="User Detail",
        description="This API is used to get the user details.(if id is not given tha output will be list of users)",
        tags=["User"],
        parameters=[
            OpenApiParameter(name="id", type=int, description="id of the user"),
        ],
        request=None,
        responses={
            200: serializer_class,
            400: error_schema,
            500: error_schema,
        }
    )
    def get(self, request):
        try:
            user_id = request.GET.get('id', None)
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return CommonUtils.dispatch_failure(request, USER_NOT_FOUND,
                                                        error_message=f"User with id '{user_id}' not found")

                serializer = self.serializer_class(user)
            else:
                users = User.objects.all()
                serializer = self.serializer_class(users, many=True)

            return CommonUtils.dispatch_success(request, serializer.data)

        except:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="User Detail",
        description="This API is used to create the user.",
        tags=["User"],
        request=serializer_class,
        responses={
            200: serializer_class,
            400: error_schema,
            500: error_schema,
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, error_message=serializer.errors)
            else:
                serializer.save()

            return CommonUtils.dispatch_success(request, serializer.data)

        except:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="User Detail",
        description="This API is used to update the user.",
        tags=["User"],
        parameters=[OpenApiParameter(name="id", type=int, description="id of the user", required=True)],
        request=serializer_class,
        responses={
            200: serializer_class,
            400: error_schema,
            500: error_schema,
        }
    )
    def patch(self, request):
        try:
            user_id = request.GET.get('id', None)
            if not user_id:
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, error_message='id is required')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return CommonUtils.dispatch_failure(request, USER_NOT_FOUND,
                                                    error_message=f"User with id '{user_id}' not found")

            username = request.data.get('username', None)
            if username:
                if username != user.username:
                    return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS,
                                                        error_message='username cannot be changed')
            else:
                request.data['username'] = user.username

            serializer = self.serializer_class(data=request.data, instance=user)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, error_message=serializer.errors)

            serializer.save()
            return CommonUtils.dispatch_success(request, serializer.data)

        except:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)
