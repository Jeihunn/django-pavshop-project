from rest_framework.routers import DefaultRouter
from core.api.views import NewsletterAPIView

router = DefaultRouter()

router.register(r'newsletters', NewsletterAPIView)
