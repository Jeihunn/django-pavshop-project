from django.urls import path, include
from core.api.views import NewsletterAPIView
from core.api.routers import router

urlpatterns = [
    path('newsletter/', NewsletterAPIView.as_view(), name='newsletter'),

]

#urlpatterns += (router.urls, "core")