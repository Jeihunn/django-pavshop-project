from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.index_view, name="index_view"),
    path("contact/", views.ContactView.as_view(), name="contact_view"),
    path("about-us/", views.about_us_view, name="about_us_view"),
]
