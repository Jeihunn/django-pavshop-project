from django.urls import path
from . import views as api_views

app_name = "api_core"
urlpatterns = [
    path("newsletter/", api_views.NewsletterCreateAPIView.as_view(),
         name="api_newsletter_create_view"),
]
