from core.models import Newsletter
from core.api.serializers import NewsletterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view


class NewsletterAPIView(CreateAPIView): 
    allowed_methods = ['POST']
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()