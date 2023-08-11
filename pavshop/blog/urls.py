from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("blogs/archive/<str:year>/<str:month>/", views.blog_archive_view, name='blog_archive_view'),
    path("blogs/", views.blog_list_view, name="blog_list_view"),
    path("blog/<slug:blog_slug>/", views.blog_detail_view, name="blog_detail_view"),
]
