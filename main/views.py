from rest_framework.request import Request
from rest_framework.response import Response

from root.utils.utils import success
from root.utils.views.api_view import APIView

# Create your views here.


class HomeAPI(APIView):
    def get(self, request: Request) -> Response:
        return Response(success())
