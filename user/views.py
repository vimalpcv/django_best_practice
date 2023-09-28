from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import OpenApiParameter, extend_schema
from functools import partial
from common.utils import CommonUtils
from common.logger import info_log, error_log
from common.permissions import IsAllowedUser, method_permission_classes
from common.constants import SUPER_ADMIN, ADMIN
from common.error import *
from user.serializer import *
from user.models import User


class UserDetailView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserDetailSerializer

    @extend_schema(
        operation_id="Get User Detail ",
        description="This API is used to get the user details.(if id is not given tha output will be list of users)",
        tags=["User"],
        parameters=[
            OpenApiParameter(name="id", type=int, description="id of the user"),
        ],
        request=None,
        responses={
            200: serializer_class,
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
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
        operation_id="Create User Detail",
        description="This API is used to create the user.",
        tags=["User"],
        request=serializer_class,
        responses={
            200: serializer_class,
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
        }
    )
    @method_permission_classes((partial(IsAllowedUser, SUPER_ADMIN),))  # it will override the permission_classes
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
        operation_id="Update User Detail",
        description="This API is used to update the user.",
        tags=["User"],
        parameters=[OpenApiParameter(name="id", type=int, description="id of the user", required=True)],
        request=serializer_class,
        responses={
            200: serializer_class,
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
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
