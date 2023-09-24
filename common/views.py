from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import OpenApiParameter, extend_schema

from common.utils import CommonUtils
from common.constants import SUCCESS
from common.logger import info_log


class HealthCheck(APIView):
    """
    API endpoint that allows to check the health of the server.
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["General"],
        responses={
            200: {"type": "string", "example": "SUCCESS"},
        }
    )
    def get(self, request):
        info_log(request, "Healthcheck Success")
        return CommonUtils.dispatch_success(request, SUCCESS)
