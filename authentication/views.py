
from drf_spectacular.utils import extend_schema
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView, RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.serializers import LoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from authentication.serializer import *
from authentication.adapter import CustomGoogleOAuth2Adapter
from common.utils import CommonUtils
from common.error import (
    ERROR_SCHEMA, INVALID_PARAMETERS, INTERNAL_SERVER_ERROR, INVALID_REFRESH_TOKEN, ACCOUNT_NOT_FOUND, BAD_REQUEST)
from common.logger import error_log


class CustomRegisterView(RegisterView):
    permission_classes = (AllowAny,)
    serializer_class = CustomRegisterSerializer

    @extend_schema(
        operation_id="Register",
        description="This API is used to register a new user.",
        tags=["Authentication"],
        request=CustomRegisterSerializer,
        responses={
            201: LoginResponseSerializer,
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            try:
                response = super().create(request, *args, **kwargs)
            except ValidationError as e:
                return CommonUtils.dispatch_failure(request, error=INVALID_PARAMETERS, data=e.detail)

            if response.status_code == 201:
                return CommonUtils.dispatch_success(request, response.data)
            else:
                return CommonUtils.dispatch_failure(request, error=INVALID_PARAMETERS, data=response.data)
        except Exception as e:
            error_log(request)
            return CommonUtils.dispatch_failure(request, error=INTERNAL_SERVER_ERROR, data=str(e))


class CustomLoginView(LoginView):

    @extend_schema(
        operation_id="Login",
        description="This API is used to login a user.",
        tags=["Authentication"],
        request=LoginSerializer,
        responses={
            201: LoginResponseSerializer,
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            try:
                response = super().post(request, *args, **kwargs)
            except ValidationError as e:
                data = e.detail['non_field_errors'][0] if e.detail.get('non_field_errors') else e.detail
                return CommonUtils.dispatch_failure(request, error=INVALID_PARAMETERS, data=data)

            if response.status_code == 200:
                return CommonUtils.dispatch_success(request, response.data)
            else:
                return CommonUtils.dispatch_failure(request, error=BAD_REQUEST, data=response.data)
        except Exception as e:
            error_log(request)
            return CommonUtils.dispatch_failure(request, error=INTERNAL_SERVER_ERROR, data=str(e))


class CustomLogoutView(LogoutView):
    serializer_class = LogoutViewSerializer

    @extend_schema(
        description="This API is used to logout a user.",
        operation_id="Logout",
        tags=["Authentication"],
        request=LogoutViewSerializer,
        responses={
            200: {
                "type": "object",
                "example": {
                    "detail": "Successfully logged out."
                }
            },
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, data=serializer.errors)

            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                return CommonUtils.dispatch_success(request, response.data)
            else:
                data = response.data['detail'] if response.data.get('detail') else response.data
                return CommonUtils.dispatch_failure(request, error=INVALID_PARAMETERS, data=data)
        except Exception as e:
            error_log(request)
            return CommonUtils.dispatch_failure(request, error=INTERNAL_SERVER_ERROR, data=str(e))


class RefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)

    @extend_schema(
        operation_id="Refresh Token",
        description="This API is used to refresh the access token.",
        tags=["Authentication"],
        request=RefreshViewSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "access": {"type": "string"}
                }
            },
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = RefreshViewSerializer(data=request.data)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, data=serializer.errors)
            try:
                response = super().post(request, *args, **kwargs)
                return CommonUtils.dispatch_success(request, {"access": response.data["access"]})
            except Exception as e:
                return CommonUtils.dispatch_failure(request, INVALID_REFRESH_TOKEN, data=str(e))
        except Exception as e:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR, data=str(e))


class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = settings.CALLBACK_URL
    client_class = OAuth2Client

    @extend_schema(
        operation_id="Google Login",
        description="This API is used to login a user using Google.",
        tags=["Authentication"],
        request={
            "application/json": {"type": "object", "properties": {"code": {"type": "string"}, }, "required": ["code"]}},
        responses={
            200: LoginResponseSerializer,
            400: ERROR_SCHEMA,
            404: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            try:
                response = super().post(request, *args, **kwargs)
            except ValidationError as e:
                data = e.detail['non_field_errors'][0] if e.detail.get('non_field_errors') else e.detail
                return CommonUtils.dispatch_failure(request, error=ACCOUNT_NOT_FOUND, data=data)
            if response.status_code == 200:
                return CommonUtils.dispatch_success(request, response.data)
            else:
                return CommonUtils.dispatch_failure(request, error=BAD_REQUEST, data=response.data)
        except Exception as e:
            error_log(request)
            return CommonUtils.dispatch_failure(request, error=INTERNAL_SERVER_ERROR, data=str(e))


class GoogleConnect(SocialConnectView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = settings.CALLBACK_URL
    client_class = OAuth2Client

    @extend_schema(
        operation_id="Google Connect",
        description="This API is used to connect a user using Google.",
        tags=["Authentication"],
        request={
            "application/json": {"type": "object", "properties": {"code": {"type": "string"}, }, "required": ["code"]}},
        responses={
            200: LoginResponseSerializer,
            400: ERROR_SCHEMA,
            500: ERROR_SCHEMA,
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            try:
                response = super().post(request, *args, **kwargs)
            except ValidationError as e:
                data = e.detail['non_field_errors'][0] if e.detail.get('non_field_errors') else e.detail
                return CommonUtils.dispatch_failure(request, error=INVALID_PARAMETERS, data=data)
            if response.status_code == 200:
                return CommonUtils.dispatch_success(request, response.data)
            else:
                return CommonUtils.dispatch_failure(request, error=BAD_REQUEST, data=response.data)
        except Exception as e:
            error_log(request)
            return CommonUtils.dispatch_failure(request, error=INTERNAL_SERVER_ERROR, data=str(e))
