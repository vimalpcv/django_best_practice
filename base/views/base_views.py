from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from base.utils import BaseUtils
from base.constants import SUCCESS
from base.logger import info_log


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
        return BaseUtils.dispatch_success(request, {"status": SUCCESS})