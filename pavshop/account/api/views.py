from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserTokenSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(responses={200: UserTokenSerializer(many=True)})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
