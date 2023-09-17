from rest_framework import generics
from rest_framework import permissions
from .serializers import NewsletterSerializer
from core.models import Newsletter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class NewsletterCreateAPIView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
