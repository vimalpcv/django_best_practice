from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import OpenApiParameter, extend_schema
from datetime import datetime
from .utils import CommonUtils
from common.serializer import TemplateViewSerializer
from common.error import *
from common.logger import info_log, error_log


class HealthCheck(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["General"],
        responses={
            200: {"type": "string", "example": "OK"},
        }
    )
    def get(self, request):
        print('HealthCheck')
        return CommonUtils.dispatch_success(request, 'OK')


class Template(APIView):

    # @extend_schema(exclude=True)
    @extend_schema(
        tags=["User"],
        parameters=[
            OpenApiParameter(name="name", type=str, description="Name of the user", required=True),
            OpenApiParameter(name="age", type=int, description="Age of the user", ),
            OpenApiParameter(name="dob", type=datetime,
                             description="Date of birth of the user (YYYY-MM-DD)", ),
            OpenApiParameter(name="sex", type=str, description="Sex of the user", enum=["Male", "Female", "Others"],
                             default='Male'),
            OpenApiParameter(name="device_type", location='header'),  # query(default), path, header, cookie
        ],
        request=TemplateViewSerializer(many=True),
        responses={
            202: {
                "type": "object",
                "example": {
                    "name": "John",
                    "age": 25,
                }
            },
            400: error_schema,
            404: error_schema,
            500: error_schema,
        }
    )
    def post(self, request):
        try:
            serializer = TemplateViewSerializer(data=request.data)
            if not serializer.is_valid():
                return CommonUtils.dispatch_failure(request, INVALID_PARAMETERS, error_message=serializer.errors)
            else:
                data = serializer.validated_data

            info_log(request, data)
            return CommonUtils.dispatch_success(request, data, status_code=200)
        except:
            error_log(request)
            return CommonUtils.dispatch_failure(request, INTERNAL_SERVER_ERROR)