from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from root.utils.utils import success

# Create your views here.


class HomeAPI(APIView):
    def get(self, request: Request) -> Response:
        return Response(success())
