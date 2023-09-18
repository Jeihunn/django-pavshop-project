from rest_framework import generics
from rest_framework import permissions
from .serializers import NewsletterSerializer
from core.models import Newsletter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from drf_yasg.utils import swagger_auto_schema


class NewsletterCreateAPIView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @swagger_auto_schema(tags=["Newsletter API"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
